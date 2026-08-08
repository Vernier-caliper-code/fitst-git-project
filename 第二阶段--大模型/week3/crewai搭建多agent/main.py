"""CrewAI 多 Agent 俄罗斯方块团队.

流水线: tetris_writer(写代码) → code_reviewer(审查+修复)
配置: config/agents.yaml + config/tasks.yaml
"""

import os
from pathlib import Path

import yaml
from crewai import LLM, Agent, Crew, Process, Task
from crewai.crews.crew_output import CrewOutput
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 1. 加载环境变量
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
# 2. 读取 YAML 配置
# ---------------------------------------------------------------------------
with open(BASE_DIR / "config" / "agents.yaml", encoding="utf-8") as f:
    agent_configs: dict = yaml.safe_load(f)

with open(BASE_DIR / "config" / "tasks.yaml", encoding="utf-8") as f:
    task_configs: dict = yaml.safe_load(f)

# ---------------------------------------------------------------------------
# 3. 构建 Agent 对象
# ---------------------------------------------------------------------------
agents: dict[str, Agent] = {}
for name, cfg in agent_configs.items():
    agents[name] = Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        verbose=cfg.get("verbose", True),
        allow_delegation=cfg.get("allow_delegation", False),
        llm=llm,
    )

# ---------------------------------------------------------------------------
# 4. 构建 Task 对象（先建无 context 的，再补 context）
# ---------------------------------------------------------------------------
tasks: dict[str, Task] = {}
for name, cfg in task_configs.items():
    agent_name: str = cfg["agent"]
    tasks[name] = Task(
        name=name,
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agents[agent_name],
    )

# 补充 context（写代码的输出 → 查代码的输入）
for name, cfg in task_configs.items():
    context_names: list[str] = cfg.get("context_from", [])
    if context_names:
        tasks[name].context = [tasks[n] for n in context_names]

# ---------------------------------------------------------------------------
# 5. 构建 Crew 并运行
# ---------------------------------------------------------------------------
crew = Crew(  # type: ignore[reportCallIssue]
    agents=list(agents.values()),
    tasks=list(tasks.values()),
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()

# ---------------------------------------------------------------------------
# 6. 保存最终输出
# ---------------------------------------------------------------------------
output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "tetris.py"

# crew.kickoff() 返回 CrewOutput | CrewStreamingOutput，用 .raw 取字符串
raw_output: str = result.raw if isinstance(result, CrewOutput) else str(result)

# 去掉可能的 markdown 代码块包裹
code = raw_output.strip()
if code.startswith("```python"):
    code = code.removeprefix("```python").removesuffix("```")
elif code.startswith("```"):
    code = code.removeprefix("```").removesuffix("```")

output_file.write_text(code.strip() + "\n", encoding="utf-8")

print(f"\n✅ 俄罗斯方块代码已保存到: {output_file}")
