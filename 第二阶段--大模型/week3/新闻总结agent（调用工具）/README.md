# 新闻总结 Agent

用 CrewAI 封装 Hacker News 公开 API（免费、无需 key），让 Agent 自主抓取头条并总结成中文要点，Pydantic 校验输出。

## 整体逻辑

一句话：**LLM 不联网、不抓数据，它只负责「决定干什么 + 把结果整理成中文」，真正联网干活的是你的 Python 函数。** 工具（`BaseTool`）就是这两个世界之间的桥。

```
用户提问
   ↓
① 装大脑        main.py 从 .env 读 DeepSeek key，构造 LLM（Agent 的大脑，此时还没有数据）
   ↓
② 工具菜单      FetchNewsTool 的 name + description + args_schema（LLM 靠这段文字决定要不要调）
   ↓
③ 自主决策      LLM 判断需要新闻 → 输出意图 JSON {"limit": 10} → 框架调 _run(limit=10)
   ↓
④ 真实抓取      _run 里调 news_service.fetch_top_stories() → 真正联网拿头条 → JSON 还给 LLM
   ↓
⑤ 总结+校验     LLM 把英文标题总结成中文要点 → 输出 JSON → output_pydantic 校验 → 失败重试 1 次
   ↓
结构化结果      result.pydantic（NewsDigest）
```

## 四步链路详解

### ① 装大脑

```python
llm = LLM(
    model="deepseek-v4-flash",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)
```

从 `.env` 读 key 和地址构造 LLM。**这里只有大脑，没有数据。**

### ② 给 LLM 一张「工具菜单」

`FetchNewsTool` 继承 `BaseTool`，三个字段就是菜单条目：

| 字段 | 作用 |
|------|------|
| `name` | 工具名 `fetch_top_stories`，LLM 记住这个名字就能点单 |
| `description` | 用中文写「这工具干嘛的、什么时候该用」——LLM 靠它决定要不要调 |
| `args_schema` | 调工具时参数长什么样（`FetchNewsInput.limit`） |

关键点：**工具本体只写了「菜名和做法」，真正执行在 `_run()` 里。**

### ③ Agent 自主决策：点单 → 上菜

用户提问 → CrewAI 把工具菜单塞给 LLM → LLM 判断"需要新闻数据" → 输出意图 JSON（如 `{"limit": 10}`）→ 框架**真的去调 `_run(limit=10)`**。

### ④ 真实抓取（Python 世界）

`_run` 里调用 `news_service.fetch_top_stories()`，真正联网：

```
请求 topstories.json → 拿约 500 个 ID → 取前 10 个 → 逐个请求详情
→ 过滤掉 type != "story" → 返回 [{title, url, score}, ...] 的 JSON 字符串给 LLM
```

> 核心记忆点：**LLM 只出意图，Python 函数干真活。** 天气示例是 mock 数据，这里是真联网，其余结构一模一样。

### ⑤ 总结 + 校验

LLM 拿到 10 条英文头条 → 按要求总结成中文一句话 → 输出 JSON → `output_pydantic=NewsDigest` 像安检一样检查字段、类型、数量 → 不符合则 `max_retry_limit=1` 自动重试一次 → 校验通过得到 `result.pydantic`。

## 两个 Pydantic 模型各管一段

| 模型 | 管什么 | 出错时 |
|------|--------|--------|
| `FetchNewsInput` | LLM 调工具时的参数 | 工具不执行 |
| `NewsSummaryItem` / `NewsDigest` | LLM 的最终输出 | 自动重试 1 次 |

## 文件结构

```
新闻总结agent/
├── .env                    # DeepSeek 配置（不提交 git）
├── .gitignore              # 忽略 .env / __pycache__
├── news_service.py         # 纯 Python 真实功能：调 HN API 抓头条（可单独运行自检）
├── main.py                 # 编排层：LLM / 工具 / Agent / Task / Pydantic 校验
└── README.md
```

为什么拆两个文件：

- `news_service.py` = **纯 Python 真实功能**，不依赖 LLM，可单独自检、单独测试
- `main.py` = **编排层**，以后换数据源（比如中文新闻 API）只改 `news_service.py` 和工具描述，不动编排逻辑

## 快速开始

```bash
# 1. 安装依赖
pip install crewai requests python-dotenv pydantic

# 2. 配置 .env（复制自 weather 示例）
# DEEPSEEK_API_KEY=sk-xxx
# DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 3. 自检抓取函数（不调 LLM，仅验证网络）
python news_service.py

# 4. 跑完整流程
python main.py
```

## 运行提示

- Windows GBK 控制台可能报 `Sync handler error: 'gbk' codec can't encode...` 和中文乱码——这是 CrewAI 内部日志打印 emoji 在 GBK 编码下失败，**纯环境噪音，不影响流程**。在 VSCode 终端（UTF-8）运行显示正常。

## 技术栈

- [CrewAI](https://crewai.com) 1.15+ — 多 Agent 编排框架
- [DeepSeek API](https://platform.deepseek.com) — LLM 后端（OpenAI 兼容端点）
- [Hacker News API](https://github.com/HackerNews/API) — 免费公开接口，无需 key
- Pydantic — 工具入参 + 输出校验
