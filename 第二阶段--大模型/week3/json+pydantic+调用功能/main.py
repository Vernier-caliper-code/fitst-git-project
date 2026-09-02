"""CrewAI 示例：JSON 输出 + Pydantic 校验 + 自定义工具调用.

全链路：用户提问 → Agent 自主调用天气工具 → 返回 JSON → Pydantic 校验 → 结构化结果

对应需求：
  1. 真实函数：weather_service.query_weather()
  2. 工具定义：BaseTool 的 name + description + args_schema
  3. Prompt JSON 约束：Task.description 里显式写明输出结构
  4. 跑通：Agent 自主调用工具并返回结构化结果
  5. 加分：output_pydantic 校验输出，失败自动重试 1 次（max_retry_limit=1）
"""

import json
import os
from pathlib import Path

from crewai import LLM, Agent, Crew, Task
from crewai.crews.crew_output import CrewOutput
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from weather_service import query_weather

# ---------------------------------------------------------------------------
# 1. 加载环境变量，配置 LLM（OpenAI 兼容端点）
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

llm = LLM(
    model="deepseek-v4-flash",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# ---------------------------------------------------------------------------
# 2. Pydantic 模型：工具入参 / 最终输出（校验 LLM 输出的"类型检查器"）
# ---------------------------------------------------------------------------


class WeatherQueryInput(BaseModel):
    """工具参数：LLM 调工具时只出这个 JSON，你的代码再执行真实函数。"""

    city: str = Field(description="要查询天气的城市名称，如：北京、上海、广州")


class WeatherReport(BaseModel):
    """最终输出结构：LLM 必须返回符合该结构的 JSON，Pydantic 负责校验。"""

    city: str = Field(description="城市名称")
    temperature: int = Field(description="当前气温（摄氏度）")
    condition: str = Field(description="天气状况，如：晴、多云、小雨")
    feels_like: int = Field(description="体感温度（摄氏度）")
    advice: str = Field(description="给用户的出行/穿衣建议")


# ---------------------------------------------------------------------------
# 3. 工具定义：name + description + parameters（给 LLM 的"菜单文字"）
# ---------------------------------------------------------------------------


class WeatherQueryTool(BaseTool):
    name: str = "weather_query"
    description: str = (
        "查询指定城市的当前天气，返回气温、天气状况、体感温度和出行建议。"
        "当用户询问某个城市的天气时，必须调用此工具。"
    )
    args_schema: type[BaseModel] = WeatherQueryInput

    def _run(self, city: str) -> str:
        """执行真实函数，返回 JSON 字符串给 LLM。"""
        data = query_weather(city)
        return json.dumps(data, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 4. Agent + Task：Prompt 里加 JSON 输出约束，校验失败重试 1 次
# ---------------------------------------------------------------------------

agent = Agent(
    role="天气查询助手",
    goal="根据用户的提问，自主判断是否需要调用天气工具，并用固定 JSON 结构返回结果",
    backstory=(
        "你是一个高效的天气助手，擅长从自然语言中提取城市名，"
        "调用工具获取数据后，严格按要求的 JSON 结构输出。"
    ),
    tools=[WeatherQueryTool()],
    llm=llm,
    verbose=True,
    max_retry_limit=1,  # 输出不符合 Pydantic 校验时，自动重试 1 次
)

task = Task(
    description=(
        "根据用户的提问：{query}\n"
        "要求：\n"
        "1. 如果需要天气数据，必须调用 weather_query 工具获取；\n"
        "2. 最终输出必须是合法的 JSON 对象，只能包含字段："
        "city, temperature, condition, feels_like, advice；\n"
        "3. 不要输出 JSON 以外的任何文字，不要用 markdown 代码块包裹。"
    ),
    expected_output="符合 WeatherReport 结构的合法 JSON 字符串",
    output_pydantic=WeatherReport,  # 结构化输出，Pydantic 校验
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

# ---------------------------------------------------------------------------
# 5. 跑通：提问 → Agent 自主调用工具 → Pydantic 校验 → 结构化结果
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = crew.kickoff(inputs={"query": "日本今天天气怎么样？"})

    # kickoff() 类型声明是 CrewOutput | CrewStreamingOutput，但非流式运行时一定是 CrewOutput。
    # 加 isinstance 收窄类型，让 Pylance 不再误报 .raw / .pydantic 属性不存在。
    if isinstance(result, CrewOutput):
        print("\n" + "=" * 60)
        print("原始输出 (result.raw)：")
        print(result.raw)
        print("=" * 60)
        print("Pydantic 校验后 (result.pydantic)：")
        print(result.pydantic)
    else:
        print("非标准输出：", result)
