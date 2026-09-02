"""CrewAI 示例：新闻总结 Agent（真实 API 抓取 + 工具调用 + Pydantic 校验）.

全链路：用户提问 → Agent 自主调用 fetch_top_stories 抓 HN 头条 → 总结成中文要点 → Pydantic 校验

对应需求：
  1. 真实函数：news_service.fetch_top_stories()
  2. 工具定义：BaseTool 的 name + description + args_schema
  3. Prompt 约束：Task.description 里显式写明输出结构
  4. 跑通：Agent 自主调用工具抓取真实头条并总结
  5. 加分：output_pydantic 校验输出，失败自动重试 1 次（max_retry_limit=1）
"""

import json
import os
from pathlib import Path

from crewai import LLM, Agent, Crew, Task
from crewai.crews.crew_output import CrewOutput
from crewai.tools import BaseTool
from dotenv import load_dotenv
from news_service import fetch_top_stories
from pydantic import BaseModel, Field

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
# 2. Pydantic 模型：工具入参 / 最终输出
# ---------------------------------------------------------------------------


class FetchNewsInput(BaseModel):
    """工具参数：LLM 调工具时只出这个 JSON，你的代码再执行真实抓取函数。"""

    limit: int = Field(default=10, description="要抓取的头条条数，默认 10")


class NewsSummaryItem(BaseModel):
    """单条头条的总结。"""

    title: str = Field(description="原标题（英文）")
    summary: str = Field(description="中文一句话要点")
    url: str = Field(description="原文链接")
    score: int = Field(description="Hacker News 点数（热度参考）")


class NewsDigest(BaseModel):
    """最终输出结构：LLM 必须返回符合该结构的 JSON，Pydantic 负责校验。"""

    items: list[NewsSummaryItem] = Field(description="头条要点列表")
    total: int = Field(description="总结条数")


# ---------------------------------------------------------------------------
# 3. 工具定义：name + description + parameters
# ---------------------------------------------------------------------------


class FetchNewsTool(BaseTool):
    name: str = "fetch_top_stories"
    description: str = (
        "抓取 Hacker News 当前的 top 头条，返回标题、原文链接和点数。"
        "当用户想了解科技新闻头条或 Hacker News 热门话题时，必须调用此工具。"
    )
    args_schema: type[BaseModel] = FetchNewsInput

    def _run(self, limit: int = 10) -> str:
        """执行真实抓取函数，返回 JSON 字符串给 LLM（网络异常时返回错误信息）。"""
        try:
            stories = fetch_top_stories(limit)
        except Exception as e:  # noqa: BLE001 - 网络异常如实告知 LLM
            return json.dumps({"error": f"抓取头条失败：{e}"}, ensure_ascii=False)
        return json.dumps(stories, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 4. Agent + Task：Prompt 里加输出约束，校验失败重试 1 次
# ---------------------------------------------------------------------------

agent = Agent(
    role="科技新闻助手",
    goal="抓取 Hacker News 头条，并用固定 JSON 结构返回中文要点总结",
    backstory=(
        "你是一个高效的科技新闻助手，擅长调用工具获取头条数据，"
        "把英文标题提炼成简洁的中文要点，严格按要求的 JSON 结构输出。"
    ),
    tools=[FetchNewsTool()],
    llm=llm,
    verbose=True,
    max_retry_limit=1,  # 输出不符合 Pydantic 校验时，自动重试 1 次
)

task = Task(
    description=(
        "根据用户的提问：{query}\n"
        "要求：\n"
        "1. 必须先调用 fetch_top_stories 工具抓取头条；\n"
        "2. 把每条头条的 title 用中文总结成一句话要点 summary；\n"
        "3. 最终输出必须是合法的 JSON 对象，只能包含字段：items, total；\n"
        "4. items 是列表，每个元素只能包含字段：title, summary, url, score；\n"
        "5. 不要输出 JSON 以外的任何文字，不要用 markdown 代码块包裹。"
    ),
    expected_output="符合 NewsDigest 结构的合法 JSON 字符串（含 items 列表和 total）",
    output_pydantic=NewsDigest,  # 结构化输出，Pydantic 校验
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)

# ---------------------------------------------------------------------------
# 5. 跑通：提问 → Agent 自主调用工具 → 总结 → Pydantic 校验 → 结构化结果
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = crew.kickoff(inputs={"query": "今天 Hacker News 上有什么值得关注的头条？请总结要点。"})

    if isinstance(result, CrewOutput):
        print("\n" + "=" * 60)
        print("原始输出 (result.raw)：")
        print(result.raw)
        print("=" * 60)
        print("Pydantic 校验后 (result.pydantic)：")
        print(result.pydantic)
    else:
        print("非标准输出：", result)
