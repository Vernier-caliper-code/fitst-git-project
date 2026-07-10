# Python 学习之路

个人 Python 学习练习仓库，按「周 / 天」组织，记录从基础语法到小项目实战的学习轨迹。每个目录对应一个学习阶段，包含练习代码、笔记和知识点总结。

## 环境

- Python 3.12.7
- 依赖标准库为主（`json`、`csv`、`os` 等），无第三方依赖
- 使用 `.venv` 虚拟环境（已在 `.gitignore` 中忽略）

```bash
# 创建并激活虚拟环境
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)

# 运行任意练习脚本
python week1/day6/todo.py
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
│
├── day4--day5/                 工具与环境
│   └── 工具和环境的进阶.md      pip / venv / uv、Git 与 GitHub
│
├── day6/                       JSON 与项目实战
│   ├── json使用.py             JSON 序列化 / 反序列化
│   └── todo.py                 命令行 TODO 管理器（小项目）
│
└── 加强点.md                   易忘知识点清单
```

## 各阶段要点

| 阶段 | 内容 |
| :--- | :--- |
| **Day 1-2** | 基础语法、流程控制、函数进阶、四大容器、类与对象、多态 |
| **Day 3** | `map`/`filter`/列表推导式、闭包、装饰器、生成器、CSV 处理、异常处理 |
| **Day 4-5** | 包管理（pip / venv / uv）、Git 与 GitHub 基础工作流 |
| **Day 6** | JSON 序列化与持久化、命令行 TODO 项目实战 |

### Day 1-2 练习题

`week1/day1-2/day1-day2练习题/` 下的 11 道基础练习：

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

`week1/day6/todo.py` 是一个综合小项目，演示了「做一个小项目」的完整流程：确定数据结构 → 选择容器 → JSON 持久化 → 编写增删改查 → 逐个修复异常。

支持功能：添加任务、列出任务、标记完成、删除任务，数据以 JSON 文件（`todo_data.json`）持久化。

```bash
python week1/day6/todo.py
```

运行后按菜单提示操作（`1` 添加 / `2` 列出 / `3` 标记完成 / `4` 删除 / `q` 退出并保存）。
