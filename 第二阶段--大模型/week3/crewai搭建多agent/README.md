# CrewAI 多 Agent 俄罗斯方块

用 CrewAI 搭建双 Agent 流水线：一个 Agent 写俄罗斯方块代码，另一个 Agent 审查并修复代码。

## 架构

```
config/agents.yaml ──┐
                     ├──→ main.py ──→ Crew(sequential) ──→ output/tetris.py
config/tasks.yaml  ──┘
```

| Agent | 职责 |
|-------|------|
| `tetris_writer` | 编写完整的 CLI 俄罗斯方块代码 |
| `code_reviewer` | 审查代码，发现并修复 bug |

`write_tetris` 任务的输出通过 `context_from` 自动作为 `review_and_fix` 的输入上下文。

## 快速开始

### 1. 安装依赖

```bash
pip install crewai pyyaml python-dotenv
```

### 2. 配置 API Key

编辑 `.env`，填入你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

### 3. 运行

```bash
python main.py
```

### 4. 查看结果

```bash
python output/tetris.py
```

## 目录结构

```
crewai搭建多agent/
├── .env                    # API Key（不提交到 git）
├── .gitignore              # 忽略 output/
├── config/
│   ├── agents.yaml         # Agent 角色定义
│   └── tasks.yaml          # 任务定义 + 流水线依赖
├── main.py                 # 入口脚本
└── output/
    └── tetris.py           # 最终输出的游戏代码
```

## 自定义

修改 YAML 配置即可调整行为，无需改 Python 代码：

- **调整 Agent 角色**：编辑 `config/agents.yaml` 中的 `role`、`goal`、`backstory`
- **调整任务要求**：编辑 `config/tasks.yaml` 中的 `description`、`expected_output`
- **添加新 Agent**：在 `agents.yaml` 和 `tasks.yaml` 中分别增加条目即可，`main.py` 会自动识别

## 技术栈

- [CrewAI](https://crewai.com) 1.15+ — 多 Agent 编排框架
- [DeepSeek API](https://platform.deepseek.com) — LLM 后端
- YAML 配置驱动，配置与代码分离
