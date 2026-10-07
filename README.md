# Python 学习之路

个人 Python 学习练习仓库，按「周 / 天」组织，记录从基础语法到 LLM 应用、再到 Web 全栈的学习轨迹。仓库分三个阶段，另有一个综合实战项目：

- `第一阶段---python基础与进阶`：Python 基础语法、面向对象、文件处理、数据分析（NumPy / Pandas / Matplotlib / Seaborn）、HTTP 与数据校验
- `第二阶段--大模型`：LLM 应用与 Agent 开发（CrewAI / OpenAI Agents SDK / 手写 RAG / LangChain / LangGraph）
- `第三阶段--FastAPI`：Web 后端入门，FastAPI 路由 / 参数校验 / 异常与中间件 / 依赖注入 / SQLAlchemy 异步 ORM
- `AI-头条`：综合实战 —— FastAPI + MySQL + Redis 后端与 Vue 3 + Vite 前端的新闻资讯 App
- `HTML+CSS`：前端基础，HTML 标签与语义化练习（笔记见 `html.txt`）

每个目录对应一个学习阶段，包含练习代码、笔记和知识点总结。

## 环境

- Python 3.12.7
- Week1 依赖标准库（`json`、`csv`、`os` 等）；Week2 引入第三方库（`numpy`、`pandas`、`matplotlib`、`seaborn`、`requests`、`pydantic`）
- 第二阶段引入 `crewai`、`openai-agents`、`langchain`/`langgraph`、`pymilvus`、`openai` 等；LLM 后端统一用 DeepSeek（OpenAI 兼容端点），各模块在各自目录的 `.env` 里配置 `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL`
- 第三阶段/AI-头条 后端引入 `fastapi` + `uvicorn`、`SQLAlchemy`（异步）+ `aiomysql`、`redis.asyncio`、`PyJWT` + `passlib[bcrypt]`（密码哈希）
- AI-头条 前端需要 Node.js，依赖 Vue 3 + Vite + Pinia + vue-router + Vant + vue-i18n + axios（见 `AI-头条/toutiao_frontend/package.json`）
- AI-头条 运行前需本机启动 MySQL（库名 `news_app`）与 Redis（默认 `localhost:6379`）
- 使用 `.venv` 虚拟环境（已在 `.gitignore` 中忽略）

```bash
# 创建并激活虚拟环境
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)

# 运行任意练习脚本（脚本用相对路径读写数据文件，需 cd 到脚本所在目录）
cd "第一阶段---python基础与进阶/week1/day6" && python todo.py
```

## 目录结构

```
week1/
├── day1-2/                     基础语法与面向对象
│   ├── 基础.py                 变量、运算符、流程控制
│   ├── 函数的进阶.py           函数、参数、返回值
│   ├── 容器/                   list / tuple / set / dict / 字符串 / 切片
│   ├── 类和对象/               类、对象、多态
│   └── day1-day2练习题/        11 道基础练习（见下）
│
├── day3/                       进阶特性与文件处理
│   ├── map-filter和列表推导式区别.py
│   ├── 闭包和装饰器和生成器/    闭包、装饰器、生成器(yield)
│   └── 处理csv文件/            CSV 读写、文件操作、异常处理
│       ├── data.csv            练习输入数据
│       └── output.csv          处理结果输出
│
├── day4--day5/                 工具与环境
│   └── 工具和环境的进阶.md      pip / venv / uv、Git 与 GitHub
│
├── day6/                       JSON 与项目实战
│   ├── json使用.py             JSON 序列化 / 反序列化
│   ├── person.json             json 使用示例数据文件
│   ├── todo.py                 命令行 TODO 管理器（小项目）
│   └── todo_data.json          TODO 数据持久化文件
│
└── 加强点.md                   易忘知识点清单
```

```
week2/
├── numpy/                    NumPy 数组基础
│   └── numpy_basics.ipynb     ndarray 创建、索引切片、广播、聚合
├── pandas/                   Pandas 数据处理
│   ├── pandas_basics.ipynb     DataFrame 基础操作
│   └── pandas_practice.ipynb   Titanic 数据清洗与分析实战
├── matplotlib&&seaborn/      数据可视化
│   ├── matplotlib_basics.py    折线/柱状/散点/饼图、子图、高清保存
│   ├── plot_demo.png           matplotlib 输出示例图
│   ├── seaborn_basics.py       热力图 / 箱线图 / pairplot
│   ├── seaborn_heatmap.png     heatmap 输出
│   ├── seaborn_boxplot.png     boxplot 输出
│   └── seaborn_pairplot.png    pairplot 输出
├── HTTP基础/                  HTTP 请求与 API
│   ├── get.py                  GET 请求与参数拼接
│   ├── post.py                 POST 请求与 JSON 数据
│   └── http_practice.py        GitHub API 仓库数据采集
├── pydantic/                 数据校验（Pydantic v2）
│   ├── pydantic_basics.py      BaseModel、Field、field_validator
│   └── pydantic-practice.py    JSON → 模型校验 → 错误格式化
└── 加强点-week2.md            NumPy 易忘点（布尔索引、axis）
```

```
第二阶段--大模型/
├── week3/                       CrewAI 多 Agent 编排
│   ├── crewai搭建多agent/        双 Agent 顺序流水线（写代码 → 审查修复），YAML 配置驱动
│   │   ├── config/agents.yaml    Agent 角色定义
│   │   ├── config/tasks.yaml     任务定义 + context_from 流水线依赖
│   │   ├── main.py               入口脚本
│   │   └── output/tetris.py     生成的俄罗斯方块代码
│   ├── json+pydantic+调用功能/    单 Agent + 工具调用 + JSON 输出 + Pydantic 校验
│   │   ├── main.py               编排层
│   │   └── weather_service.py    mock 天气查询函数
│   └── 新闻总结agent（调用工具）/  真实联网抓 Hacker News 头条 → 中文总结
│       ├── main.py               编排层
│       └── news_service.py       纯 Python 抓取函数（可单独自检）
├── week4/                       OpenAI Agents SDK + 手写 RAG
│   ├── openai-SDK/
│   │   └── demo.py               多 Agent + Handoff 交接 + Guardrails 护栏
│   └── rag-demo/                 手写 RAG 最小 demo（切分 → TF-IDF → 余弦检索 → 生成）
│       ├── rag.py                全部手写，无第三方检索库
│       ├── data.txt              示例文档
│       └── 笔记.md               四步原理笔记 + 两种切分策略对比
├── week5/                       LangChain 全家桶
│   ├── langchain_llm.ipynb       LLM 调用 / message / 提示词模板 / Tool calling / 结构化输出
│   ├── Rag.ipynb                 文档加载器 / 文本切分 / 向量化 / Milvus / RAG 实战
│   ├── langchain_agent.ipynb     create_agent / 中间件 / hooks / 短期+长期记忆
│   ├── langsmith.ipynb           LangSmith 追踪练习
│   ├── data/                     多格式示例文档（txt/csv/json/pdf/docx）
│   └── 零基础学Milvus向量数据库.docx
└── 实战/                        两个完整项目
    ├── agentic-rag/              LangGraph 的 Agentic RAG（路由 / 评分 / 幻觉检测 / 联网兜底）
    └── documentation-helper-main/ LangChain + Tavily + Pinecone 文档助手 Streamlit 应用
```

```
第三阶段--FastAPI/
├── main.py                     FastAPI 基础：路径/查询/请求体参数、异常、中间件、依赖注入
├── ORM.py                      SQLAlchemy 2.0 异步 ORM：声明式基类、模型映射、建表、增删改查
└── test_orm.py                 ORM 练习：Users 表定义与建表
```

```
AI-头条/                          新闻资讯 App（前后端分离）
├── toutiao_backend/              FastAPI 后端
│   ├── main.py                   应用入口：CORS 中间件 + 注册路由 + 全局异常处理
│   ├── config/                   db_conf.py（异步 MySQL 引擎/会话依赖）、cache_conf.py（Redis 连接与缓存读写）
│   ├── models/                   数据库模型：users / news / favorite / history
│   ├── schemas/                  Pydantic 请求响应模型（base / users / favorite / history）
│   ├── crud/                     数据访问层：users / news / favorite / history / news_cache
│   ├── cache/news_cache.py       新闻缓存层（Redis + 数据库回源）
│   ├── routers/                  路由：news（/api/news）、users（/api/user）、favorite、history
│   ├── utils/                    security（bcrypt 哈希）、auth（Bearer Token 鉴权）、response、exception
│   └── test_main.http            接口调试用例
└── toutiao_frontend/             Vue 3 前端
    ├── src/views/                Login / Register / Home / NewsDetail / History / Favorite /
    │                             Category / AIChat / My / Profile / Settings
    ├── src/components/           NewsItem（新闻卡片）、TabBar（底部导航）
    ├── src/store/                Pinia：user / news / favorite / history / theme / language
    ├── src/i18n/                 中英文语言包（zh-CN / en-US）
    ├── src/config/api.js         后端地址与 AI 问答参数
    └── vite.config.js            /api 代理到 http://127.0.0.1:8000
```

## 各阶段要点

| 阶段 | 内容 |
| :--- | :--- |
| **Day 1-2** | 基础语法、流程控制、函数进阶、四大容器、类与对象、多态 |
| **Day 3** | `map`/`filter`/列表推导式、闭包、装饰器、生成器、CSV 处理、异常处理 |
| **Day 4-5** | 包管理（pip / venv / uv）、Git 与 GitHub 基础工作流 |
| **Day 6** | JSON 序列化与持久化、命令行 TODO 项目实战 |

### Week2 各阶段要点

| 模块 | 内容 |
| :--- | :--- |
| **NumPy** | ndarray 创建与属性、索引切片、布尔索引、广播机制、聚合操作（axis）、reshape/flatten |
| **Pandas** | DataFrame 加载/查询/排序、缺失值处理、groupby、apply、merge；Titanic 实战 |
| **Matplotlib** | 折线图、柱状图、散点图、饼图、子图布局、高分辨率保存 |
| **Seaborn** | 热力图（相关性）、箱线图（异常值）、pairplot（特征关系） |
| **HTTP 基础** | `requests` GET/POST、参数拼接、JSON 响应解析、GitHub API 实战 |
| **Pydantic** | `BaseModel`、`Field` 约束、`field_validator` 自定义验证、JSON → 模型校验 |

### Week3 各阶段要点（CrewAI 多 Agent）

| 模块 | 内容 |
| :--- | :--- |
| **crewai 搭建多 agent** | YAML 配置驱动、双 Agent 顺序流水线、`context_from` 传递上下文、`Process.sequential` |
| **json + pydantic + 调用功能** | `BaseTool` 工具定义、`output_pydantic` 结构化输出、`max_retry_limit` 校验失败重试 |
| **新闻总结 agent** | 真实 API 抓取、编排层与功能层分离、Pydantic 双模型（工具入参 + 最终输出） |

### Week4 各阶段要点

| 模块 | 内容 |
| :--- | :--- |
| **openai-SDK** | OpenAI Agents SDK、多 Agent + `handoff` 交接、`InputGuardrail`/`OutputGuardrail` 护栏、DeepSeek 兼容端点配置 |
| **手写 RAG** | 切分（定长滑动窗口 + overlap）、手写 TF-IDF（单字 + 相邻双字）、手写余弦相似度、两种切分策略对比实验 |

### Week5 各阶段要点（LangChain）

| 模块 | 内容 |
| :--- | :--- |
| **langchain_llm** | `invoke`/`ainvoke`/`stream`/`batch`、四种 message 角色、多轮对话与历史裁剪、`ChatPromptTemplate`（`partial`/`MessagesPlaceholder`）、Tool calling（parse_docstring / pydantic / json_schema）、`with_structured_output` |
| **Rag** | `BaseLoader` 各文档加载器、`RecursiveCharacterTextSplitter` 与语义切分、`init_embeddings` 向量化、Milvus（DDL/DML/DQL）、RAG 实战闭环 |
| **langchain_agent** | `create_agent`、LLM 与 Agent 调工具的区别、中间件（`SummarizationMiddleware` 等）、hooks、短期记忆（`InMemorySaver` + `thread_id`）与长期记忆（`Store`） |
| **langsmith** | LangSmith 追踪配置与 Web UI 查看 |

### 实战项目要点

| 项目 | 内容 |
| :--- | :--- |
| **Agentic RAG（LangGraph）** | 路由 → 检索 → 文档评分 → 决策（生成 / 联网搜索）→ 幻觉检测 → 答案评分，含 `chains` / `nodes` / `tests` |
| **Documentation Helper** | LangChain + Tavily 爬取 + Pinecone 向量库 + Streamlit 前端的文档助手（外部课程项目） |

### 第三阶段要点（FastAPI）

| 模块 | 内容 |
| :--- | :--- |
| **main.py** | 路径参数 `Path` / 查询参数 `Query` / 请求体 `BaseModel`、响应类型（`HTMLResponse` / `FileResponse`）、`HTTPException` 异常处理、中间件执行顺序（自下而上）、`Depends` 依赖注入 |
| **ORM.py** | SQLAlchemy 2.0 异步：`create_async_engine` + `async_sessionmaker`、`DeclarativeBase` 声明式基类、`Mapped` / `mapped_column` 类型映射、`insert_default` 与 `onupdate` 自动时间戳、启动时建表 |
| **test_orm.py** | 练习：定义 `Users` 表（id / username / password）并建表 |

### AI-头条 要点

| 模块 | 内容 |
| :--- | :--- |
| **后端架构** | 分层：`routers`（路由）→ `crud`（数据访问）→ `models`（表模型）；`schemas` 管请求响应结构，`config` 管连接，`utils` 放通用能力 |
| **数据库** | MySQL + `SQLAlchemy` 异步引擎，`get_db` 依赖注入负责会话开关与事务提交/回滚 |
| **缓存** | Redis 缓存新闻分类与列表，`cache/news_cache.py` 做「缓存优先 + 数据库回源」；`set_cache` 支持字符串与 JSON，带过期时间 |
| **认证** | `passlib` + `bcrypt` 哈希密码，登录发放 Token，`utils/auth.py` 的 `get_current_user` 从 `Authorization: Bearer` 解析并校验 |
| **前端** | Vue 3 + Vite + Pinia（持久化）+ vue-router，移动端组件库 Vant，`vue-i18n` 中英双语，主题切换 |
| **AI 问答** | `AIChat.vue` 前端直连 DeepSeek 接口，用 `marked` + `dompurify` 渲染 Markdown 回答 |

### Day 1-2 练习题

`第一阶段---python基础与进阶/week1/day1-2/day1-day2练习题/` 下的 11 道基础练习：

1. 质数筛（prime sieve）
2. 字符串反转
3. 词频统计
4. FizzBuzz
5. 回文判断
6. 列表操作
7. 阶乘
8. 字典合并
9. 矩阵转置
10. 银行账户类
11. 二分查找

## 项目实战：命令行 TODO 管理器

`第一阶段---python基础与进阶/week1/day6/todo.py` 是一个综合小项目，演示了「做一个小项目」的完整流程：确定数据结构 → 选择容器 → JSON 持久化 → 编写增删改查 → 逐个修复异常。

支持功能：添加任务、列出任务、标记完成、删除任务，数据以 JSON 文件（`todo_data.json`）持久化。

```bash
cd "第一阶段---python基础与进阶/week1/day6" && python todo.py
```

运行后按菜单提示操作（`1` 添加 / `2` 列出 / `3` 标记完成 / `4` 删除 / `q` 退出并保存）。

## 数据校验：Pydantic

`第一阶段---python基础与进阶/week2/pydantic/` 演示了「从 JSON 到类型安全数据」的完整校验流程：

- **`pydantic_basics.py`** — `Person` 模型，展示 `Field(frozen=True, lt=200)` 约束、`default_factory` 避免列表共享、`field_validator` 自定义校验手机号
- **`pydantic-practice.py`** — `User` 模型 + `parse_and_validate()` 将 JSON 字符串解析为类型安全对象，`_format_errors()` 把 `ValidationError` 格式化为可读错误报告

```bash
python "第一阶段---python基础与进阶/week2/pydantic/pydantic-practice.py"
```

正确数据通过校验打印详情；错误数据逐字段报告失败原因，一次返回所有错误。

---

## 多 Agent 编排：CrewAI（Week3）

`第二阶段--大模型/week3/` 用 CrewAI 搭建多 Agent 流水线，三个示例层层递进：

- **`crewai搭建多agent/`** — 双 Agent 顺序流水线：`tetris_writer` 写俄罗斯方块代码 → `code_reviewer` 审查修复，YAML 配置驱动，`context_from` 自动把上游任务输出喂给下游。
- **`json+pydantic+调用功能/`** — 单 Agent + 天气工具：`BaseTool` 定义工具菜单，`output_pydantic` 校验 LLM 返回的 JSON，`max_retry_limit=1` 校验失败自动重试。
- **`新闻总结agent（调用工具）/`** — 真实联网：Agent 自主调 `fetch_top_stories` 抓 Hacker News 头条 → 总结成中文要点。编排层（`main.py`）与功能层（`news_service.py`，可单独自检）分离。

> 核心记忆点：**LLM 只出「意图 JSON」，真正联网 / 干活的是 Python 函数；工具（`BaseTool`）是两个世界之间的桥。**

## 手写 RAG：从零实现检索增强生成（Week4）

`第二阶段--大模型/week4/rag-demo/rag.py` 不用任何第三方检索 / 切分库，把 RAG 四步全手写一遍：

| 步骤 | 函数 | 做法 |
| :--- | :--- | :--- |
| 切分 | `chunk_text()` | 定长滑动窗口 + overlap（防句子被腰斩） |
| 向量化 | `tfidf_vectors()` | 手写 TF-IDF，term 用「单字 + 相邻双字」 |
| 检索 | `cosine_similarity()` | 手写点积 / 范数，全量算余弦取 top-3 |
| 生成 | `generate_answer()` | 检索片段拼进 prompt 交 DeepSeek（缺 key 可离线） |

`run_experiment()` 对比「无重叠 vs 有重叠」两种切分，直观看出 overlap 让被切坏的答案句完整落回同一块。详见 `笔记.md`。

## Agentic RAG：LangGraph 自适应检索（实战）

`第二阶段--大模型/实战/agentic-rag/` 用 LangGraph 实现 Reflective / Self / Adaptive RAG，在朴素 RAG 上加了「判断」环节：

```
路由问题 ──→ 检索 ──→ 文档评分 ──→ 全相关？──→ 生成 ──→ 幻觉检测 ──→ 答案评分 ──→ useful: 结束
            │                          │                      │
            └──→ 联网搜索 ←── 不全相关 ←─┘  ←── 不落地 / 没用 ←──┘
```

- `graph/chains/`：`question_router`（路由）、`retrieval_grader`（文档评分）、`hallucination_grader`（幻觉检测）、`answer_grader`（答案评分）
- `graph/nodes/`：`retrieve` / `grade_documents` / `generate` / `web_search`
- 条件边驱动自适应：检索不全相关就转联网搜索，生成不落地就重试，答案跑题就转联网。

`第二阶段--大模型/实战/documentation-helper-main/` 则是一个完整的外部课程项目：LangChain + Tavily 爬取 + Pinecone 向量库 + Streamlit 前端的文档问答助手。

---

## 综合实战：AI-头条（前后端分离）

`AI-头条/` 是一个完整的新闻资讯 App，把第三阶段的 FastAPI 知识落地成有分层、有缓存、有鉴权的真实后端，再配一个 Vue 3 移动端前端。

### 功能

- 新闻：分类浏览、分页列表（返回 `hasMore`）、详情页
- 收藏与浏览历史：增 / 查 / 删 / 清空
- 用户：注册、登录、改密、个人信息，Token 鉴权
- AI 问答：前端直连 DeepSeek，Markdown 渲染回答
- 体验：中英双语（vue-i18n）、明暗主题、Pinia 持久化

### 运行

```bash
# 前置：本机启动 MySQL（库名 news_app）与 Redis（localhost:6379）

# 1. 后端
cd "AI-头条/toutiao_backend"
uvicorn main:app --reload          # http://127.0.0.1:8000

# 2. 前端（新开一个终端）
cd "AI-头条/toutiao_frontend"
npm install
npm run dev                        # Vite 通过 /api 代理到后端，无需额外跨域配置
```

### 分层结构

```
routers/  → 定义接口、参数校验、调用 crud
crud/     → 封装数据库操作（news / users / favorite / history）
models/   → SQLAlchemy 表模型
schemas/  → Pydantic 请求 / 响应模型
config/   → MySQL 引擎与 Redis 客户端
utils/    → 认证、密码哈希、统一响应、全局异常处理
```

> 主要接口：`GET /api/news/categories`（分类）、`GET /api/news/list`（分页列表）、`POST /api/user/register`（注册）等，其余见 `test_main.http`。

> ⚠️ **安全提示**：`toutiao_frontend/src/config/api.js` 中硬编码了 DeepSeek API Key 并已提交到仓库，建议改为从环境变量（`import.meta.env.VITE_*`）读取，并轮换该 Key。
