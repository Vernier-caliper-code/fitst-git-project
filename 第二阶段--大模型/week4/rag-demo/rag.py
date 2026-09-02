"""手写 RAG 最小 demo：切分 → 向量化 → 检索 → 生成（核心三步全部从零实现）.

对应需求：
  1. 切分：自己写 chunk_text()，固定字符数切块 + 重叠 overlap（不用任何切分库）
  2. 向量化：自己写 TF-IDF（不引 jieba，按"单字+相邻双字"做 term）
  3. 检索：自己写余弦相似度（点积、范数全部手写，不用 numpy）
  4. 对比：同一问题，测「无重叠」vs「有重叠」两种切分策略，观察检索片段差异
  5. 生成：检索到的段落拼进 prompt 交给 DeepSeek（可离线，缺 key 自动跳过）

运行：python rag.py   （data.txt 里的示例文档可随意替换成自己的文档）
"""

import math
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ===========================================================================
# 第 0 步：读文档（RAG 的意义就是让模型学会"引用外部知识"）
# ===========================================================================


def load_doc() -> str:
    with open(BASE_DIR / "data.txt", encoding="utf-8") as f:
        return f.read()


# ===========================================================================
# 第 1 步：切分（Chunking）
#
# 原理：文档太长塞不进 LLM 上下文，要切成小段。最简单也最本质的做法是
#   "定长滑动窗口"——每块固定 chunk_size 个字符，下一块往回退 overlap 个字符。
#   overlap 的作用：防止一个完整句子正好被切在块边界上，导致内容被腰斩。
#
#   [0 ────── 60] chunk0
#        [40 ──────── 100]  chunk1   ← 起始位置 = 60 - 20 = 40
#              [80 ──────── 140] chunk2
#   区间 [40:60] 同时属于 chunk0 和 chunk1，就是"重叠区"。
# ===========================================================================


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[tuple[int, str]]:
    """按固定字符数切块，带重叠。返回 [(字符起点, 块内容), ...]。

    Args:
        text: 整篇文档。
        chunk_size: 每块字符数。
        overlap: 相邻块之间重叠的字符数（< chunk_size）。
    """
    stride = chunk_size - overlap  # 下一块相对上一块的"前进距离"
    if stride <= 0:
        raise ValueError("overlap 必须小于 chunk_size")

    n = len(text)
    result: list[tuple[int, str]] = []
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        if chunk.strip():  # 跳过空白块
            result.append((start, chunk))
        if end == n:  # 切到文档末尾就结束
            break
        start += stride
    return result


# ===========================================================================
# 第 2 步：向量化（手写 TF-IDF）
#
# 原理：计算机不认识文字，只认识数字，所以要把每段文字变成一个"向量"。
#   TF（词频）     ：一个词在这段里出现得多，说明它重要。
#   IDF（逆文档频率）：一个词在所有段落里都出现（如"的""了"），说明它没区分度，要压低。
#   最终每个词的分量 = TF × IDF，整段文字 = 一个长度等于词表大小的向量。
#
#   term（词元）怎么切？不引 jieba，用最简单可行的方案：
#     中文按「单字 + 相邻双字」。"退款到账" → 退/款/到/账 + 退款/款到/到账
#     双字能抓住"退款"这种有含义的词，比单字强很多。
# ===========================================================================


def tokenize(text: str) -> list[str]:
    """把文本切成 term 列表：单字 + 相邻双字。isalnum() 顺手滤掉标点和空白。"""
    chars = [c for c in text if c.isalnum()]  # 只保留中文/字母/数字
    terms = list(chars)
    terms += [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]
    return terms


def build_vocab(chunks: list[str]) -> dict[str, int]:
    """扫描所有段落，收集出现过的 term，构建词表 term -> 索引。"""
    vocab: dict[str, int] = {}
    for chunk in chunks:
        for term in tokenize(chunk):
            if term not in vocab:
                vocab[term] = len(vocab)
    return vocab


def tfidf_vectors(chunks: list[str], vocab: dict[str, int]) -> tuple[list[list[float]], list[float]]:
    """手写 TF-IDF。返回 (每段的稠密向量, idf 列表)。

    tf  = 词在段内出现次数 / 段的 term 总数（归一化，抵消长短差异）
    idf = log(N / (1 + df)) + 1     N=总段数，df=含该词的段数；（+1 是平滑，防止除 0）
    """
    n = len(chunks)
    vsize = len(vocab)

    # 先算 df：每个词出现在多少个段落里
    df = [0] * vsize
    for chunk in chunks:
        for term in set(tokenize(chunk)):
            df[vocab[term]] += 1
    idf = [math.log(n / (1.0 + df[i])) + 1.0 for i in range(vsize)]

    vectors: list[list[float]] = []
    for chunk in chunks:
        terms = tokenize(chunk)
        tf = [0] * vsize
        for term in terms:
            tf[vocab[term]] += 1
        if terms:
            tf = [c / len(terms) for c in tf]
        vectors.append([tf[i] * idf[i] for i in range(vsize)])
    return vectors, idf


def query_vector(query: str, vocab: dict[str, int], idf: list[float]) -> list[float]:
    """把问题也向量化：用训练好的词表和 idf，只算这个句子的 tf。"""
    terms = tokenize(query)
    v = [0] * len(vocab)
    for term in terms:
        if term in vocab:  # 问题里出现但词表里没有的词，直接忽略
            v[vocab[term]] += 1
    if terms:
        v = [c / len(terms) for c in v]
    return [v[i] * idf[i] for i in range(len(vocab))]


# ===========================================================================
# 第 3 步：检索（手写余弦相似度）
#
# 原理：两段文字越像，向量夹角越小，cos 越接近 1。
#   cos(a,b) = (a·b) / (|a|·|b|)        —— 点积 / 两个向量长度的乘积
#   好处：自动消掉向量长度的影响，只看"方向"。长短不同的句子也能公平比较。
# ===========================================================================


def dot(a: list[float], b: list[float]) -> float:
    """手写点积：对应位置相乘再求和。"""
    return sum(x * y for x, y in zip(a, b))


def norm(v: list[float]) -> float:
    """手写向量长度（欧几里得范数）。"""
    return sum(x * x for x in v) ** 0.5


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """cos = (a·b) / (|a|·|b|)。分母为 0（零向量）时返回 0。"""
    denom = norm(a) * norm(b)
    if denom == 0:
        return 0.0
    return dot(a, b) / denom


def retrieve(
    query: str,
    chunks: list[str],
    vectors: list[list[float]],
    idf: list[float],
    vocab: dict[str, int],
    top_k: int = 3,
) -> list[tuple[float, int]]:
    """把问题向量化，和每一段算余弦相似度，返回相似度最高的 top_k 个 (分数, 段落下标)。"""
    qv = query_vector(query, vocab, idf)
    scored = sorted(
        ((cosine_similarity(qv, vec), i) for i, vec in enumerate(vectors)),
        key=lambda x: x[0],
        reverse=True,
    )
    return scored[:top_k]


# ===========================================================================
# 第 4 步：生成（DeepSeek，可离线）
#
# 原理：上面检索出的段落就是"上下文"（context）。把它拼进 prompt 里，
#   再抛问题给 LLM，让它"只根据这些资料回答"——这就是 RAG 的"生成"。
# ===========================================================================


def generate_answer(question: str, context: str, model: str = "deepseek-v4-flash") -> str | None:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL")
    if not api_key:
        print("  [跳过生成] 未找到 DEEPSEEK_API_KEY（缺 .env），检索对比部分可离线运行")
        return None

    client = OpenAI(base_url=base_url, api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是问答助手。只能根据提供的资料回答，资料里没有的信息就直说不知道，不要编造。",
            },
            {"role": "user", "content": f"资料：\n{context}\n\n问题：{question}"},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content


# ===========================================================================
# 5. 对比实验：同一问题，两种切分策略
# ===========================================================================


def build_pipeline(
    doc: str, chunk_size: int, overlap: int
) -> tuple[list[tuple[int, str]], list[str], dict[str, int], list[list[float]], list[float]]:
    """切分 → 向量化 一条龙，返回 (spans, chunks, vocab, vectors, idf)。"""
    spans = chunk_text(doc, chunk_size, overlap)
    chunks = [text for _, text in spans]
    vocab = build_vocab(chunks)
    vectors, idf = tfidf_vectors(chunks, vocab)
    return spans, chunks, vocab, vectors, idf


def run_experiment(doc: str, question: str) -> None:
    strategies = [
        ("策略A：chunk=60, overlap=0  （无重叠）", 60, 0),
        ("策略B：chunk=60, overlap=20 （有重叠）", 60, 20),
    ]
    results = {}
    for title, chunk_size, overlap in strategies:
        spans, chunks, vocab, vectors, idf = build_pipeline(doc, chunk_size, overlap)
        print("\n" + "=" * 70)
        print(f"{title}  共切出 {len(chunks)} 块")
        print(f"检索问题：「{question}」 top-3：")
        hits = retrieve(question, chunks, vectors, idf, vocab, top_k=3)
        results[title] = (spans, hits)
        for score, i in hits:
            start, text = spans[i]
            end = start + len(text)
            print(f"\n  [字符区间 {start}:{end}]  相似度 {score:.4f}")
            print(f"    {text}")
    print("\n" + "=" * 70)
    print("【差异解读】答案句「审核通过后一般三个工作日左右原路退回您的支付账户」")
    print("  被刻意放在了 60 字符边界附近：")
    print("  - 策略A（无重叠）：答案句被切在块边界上——前面一块以「…退回您的支」结尾，")
    print("    后面一块以「付账户。…」开头，检索到的上下文是残缺的两截。")
    print("  - 策略B（有重叠）：重叠区让整句完整落在同一块里，检索到的上下文完整可用。")
    print("  → 这就是 overlap 的意义：宁可让相邻块重复，也不让语义被切坏。")


if __name__ == "__main__":
    doc = load_doc()
    print(f"文档长度：{len(doc)} 字符")
    print("=" * 70)
    print("第 1~3 步（切分 → 向量化 → 检索）：")
    run_experiment(doc, question="退款多久到账？")

    print("\n" + "=" * 70)
    print("第 4 步（生成）：用策略B（有重叠）检索到的上下文，交给 DeepSeek 生成回答")
    spans, chunks, vocab, vectors, idf = build_pipeline(doc, chunk_size=60, overlap=20)
    hits = retrieve("退款多久到账？", chunks, vectors, idf, vocab, top_k=3)
    context = "\n".join(chunks[i] for _, i in hits)
    print("\n拼给模型的资料：\n")
    print(context)
    answer = generate_answer("退款多久到账？", context)
    if answer:
        print("\nDeepSeek 生成的回答：")
        print("  " + answer)
