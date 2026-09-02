"""OpenAI Agents SDK 最小 demo：多 Agent + Handoff（交接）+ Guardrails（护栏）.

全链路：用户提问 → triage 前台调度 → guardrail 检查 → handoff 交接给专家 agent → 最终回复

对应需求：
  1. 多 agent：triage（调度）+ 退款 / 物流 / 通用 三个专家
  2. handoff：triage 通过 Agent(handoffs=[...]) 声明可交接对象，运行时打印交接链
  3. guardrails：输入护栏（拦截敏感词）+ 输出护栏（拦截密钥/内部信息泄漏）
  4. 跑通：DeepSeek 兼容端点（沿用 week3 的 DEEPSEEK_BASE_URL / DEEPSEEK_API_KEY）

注意点（DeepSeek 兼容）：
  - SDK 默认走 Responses API，非 OpenAI 端点必须 set_default_openai_api("chat_completions")
  - 用 AsyncOpenAI 客户端注入自定义 base_url
  - guardrail 用纯 Python 规则而非二次 LLM 调用（规则版 100% 可跑通、速度快；
    想换 LLM 版可把 guardrail 函数改为调 Runner.run_sync(某 agent, input, output_type=...)，
    但 DeepSeek 对 json_schema 结构化输出兼容不稳，需自行测试）
"""

import os
from pathlib import Path

from agents import (
    Agent,
    GuardrailFunctionOutput,
    HandoffOutputItem,
    InputGuardrail,
    OutputGuardrail,
    RunConfig,
    Runner,
    handoff,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from dotenv import load_dotenv
from openai import AsyncOpenAI

# ---------------------------------------------------------------------------
# 1. 加载环境变量，配置 DeepSeek 兼容端点
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MODEL = "deepseek-v4-flash"

client = AsyncOpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)
set_default_openai_client(client, use_for_tracing=False)  # 不给 DeepSeek 上传 tracing
set_default_openai_api("chat_completions")                # 关键：非 OpenAI 端点必须切
set_tracing_disabled(True)

# ---------------------------------------------------------------------------
# 2. Guardrails（护栏）：纯 Python 规则，命中 tripwire 立即终止执行
# ---------------------------------------------------------------------------
# 输入护栏：拦截敏感/恶意关键词
BLOCKED_WORDS = ["傻逼", "去死", "操你", "垃圾客服", "投诉你全家", "违法", "毒品", "赌博"]

# 输出护栏：拦截内部信息泄漏（密钥、请求头等）
LEAK_MARKERS = ["sk-", "api_key", "Authorization", "Bearer ", "DEEPSEEK_API_KEY"]


def _as_text(input_data: str | list) -> str:
    """把 guardrail 收到的输入统一转成字符串（可能传 str，也可能传消息列表）。"""
    if isinstance(input_data, str):
        return input_data
    return " ".join(str(m) for m in input_data)


def check_input(ctx, agent, input_data) -> GuardrailFunctionOutput:
    """输入护栏：用户消息含敏感词 → 触发 tripwire，拒绝处理。"""
    text = _as_text(input_data)
    for word in BLOCKED_WORDS:
        if word in text:
            return GuardrailFunctionOutput(
                output_info=f"检测到敏感词「{word}」，已拦截", tripwire_triggered=True
            )
    return GuardrailFunctionOutput(output_info="输入通过", tripwire_triggered=False)


def check_output(ctx, agent, output) -> GuardrailFunctionOutput:
    """输出护栏：模型回复泄漏密钥/内部信息 → 触发 tripwire，拦截结果。"""
    text = str(output)
    for marker in LEAK_MARKERS:
        if marker in text:
            return GuardrailFunctionOutput(
                output_info=f"检测到疑似内部信息「{marker}」，已拦截", tripwire_triggered=True
            )
    return GuardrailFunctionOutput(output_info="输出通过", tripwire_triggered=False)


# ---------------------------------------------------------------------------
# 3. 多 Agent：三个专家 + triage 调度（handoff 交接）
# ---------------------------------------------------------------------------

refund_agent = Agent(
    name="退款专员",
    handoff_description="专门处理退款、退货、退款没到账的问题",
    instructions=(
        "你是电商平台的退款专员，只处理退款相关请求。"
        "引导用户说明退款原因和订单号，说明退款流程、到账时间（一般 3~7 个工作日），"
        "不要回答退款以外的问题。用简洁友好的中文回复。"
    ),
    model=MODEL,
)

shipping_agent = Agent(
    name="物流专员",
    handoff_description="专门处理物流、快递、订单发货、签收问题",
    instructions=(
        "你是电商平台的物流专员，只处理物流相关问题。"
        "根据用户提供的订单号给出物流状态，解释物流异常的常见原因和处理办法，"
        "不要回答物流以外的问题。用简洁友好的中文回复。"
    ),
    model=MODEL,
)

general_agent = Agent(
    name="通用客服",
    handoff_description="处理退款、物流以外的其他所有问题（如商品咨询、活动、优惠）",
    instructions=(
        "你是电商平台的通用客服，处理退款、物流以外的所有问题，如商品咨询、"
        "优惠活动、账号问题等。用简洁友好的中文回复。"
    ),
    model=MODEL,
)

triage_agent = Agent(
    name="前台调度",
    handoff_description="接收所有用户消息的入口，负责判断问题类型并交接给对应专家",
    instructions=(
        "你是电商客服中心的前台调度员。你的职责是判断用户问题的类型，"
        "然后立刻把对话交接给对应的专家 agent（你本人不直接回答）：\n"
        "- 退款 / 退货 / 钱没到账 → 交接给「退款专员」\n"
        "- 物流 / 快递 / 发货 / 签收 → 交接给「物流专员」\n"
        "- 其他所有问题 → 交接给「通用客服」\n"
        "判断类型后立即调用对应的 handoff 工具，不要自己回答用户。"
    ),
    model=MODEL,
    # handoff 工具名必须是合法函数名（ASCII）。agent 名是中文时，SDK 会把它改写成
    # transfer_to_____ 导致三个工具重名、LLM 无法区分，所以这里显式覆盖成唯一 ASCII 名。
    handoffs=[
        handoff(refund_agent, tool_name_override="transfer_to_refund"),
        handoff(shipping_agent, tool_name_override="transfer_to_shipping"),
        handoff(general_agent, tool_name_override="transfer_to_general"),
    ],
    # 输入护栏挂在入口 agent 上（SDK 只在第一轮跑 starting_agent 的输入护栏，正好符合"入口把关"）
    input_guardrails=[InputGuardrail(check_input, name="敏感词输入护栏", run_in_parallel=False)],
)

# ---------------------------------------------------------------------------
# 4. 跑通：4 个典型场景
# ---------------------------------------------------------------------------


# 输出护栏放 RunConfig 层：无论 handoff 后哪个 agent 产出最终回复，都会过一遍护栏。
# （注意：如果挂在 triage 上就是死代码——triage 在 handoff 场景里从不产生最终输出。）
RUN_CONFIG = RunConfig(output_guardrails=[OutputGuardrail(check_output, name="防泄漏输出护栏")])


def run_case(title: str, query: str) -> None:
    """跑一个输入：打印交接链 + 最终回复；被护栏拦截则打印拦截原因。"""
    print("\n" + "=" * 60)
    print(f"[{title}] 用户：{query}")
    try:
        result = Runner.run_sync(triage_agent, query, run_config=RUN_CONFIG)
        # 从运行记录里找出 handoff 交接项，打印完整交接链
        for item in result.new_items:
            if isinstance(item, HandoffOutputItem):
                print(f"  -> [handoff] {item.source_agent.name} -> {item.target_agent.name}")
        print(f"  [最终回复] {result.final_output}")
    except InputGuardrailTripwireTriggered as e:
        print(f"  [输入护栏拦截] {e.guardrail_result.output.output_info}")
    except OutputGuardrailTripwireTriggered as e:
        print(f"  [输出护栏拦截] {e.guardrail_result.output.output_info}")


if __name__ == "__main__":
    run_case("场景1: 输入护栏拦截", "你们客服都是傻逼，我要投诉你们全家！")
    run_case("场景2: handoff → 退款专员", "我刚买的手机想退货，钱什么时候能退回来？")
    run_case("场景3: handoff → 物流专员", "我的快递三天没更新了，订单号是123456，帮我查查")
    run_case("场景4: handoff → 通用客服", "你们店里有什么手机优惠活动吗？")

    # 场景5: 输出护栏逻辑自测 —— 不走 LLM，直接喂给护栏函数一个"泄漏密钥"的假回复，
    # 确定性演示输出护栏能拦下。真实运行中模型主动泄漏的概率很低，所以单独测逻辑。
    print("\n" + "=" * 60)
    print("[场景5: 输出护栏逻辑自测]")
    guard_out = check_output(None, triage_agent, "好的，你的密钥是 sk-abcdef123456，请保密")
    print(f"  [输出护栏] tripwire_triggered={guard_out.tripwire_triggered}, {guard_out.output_info}")
