"""
【问题】字典词频统计
  给一段英文文本，统计每个单词出现的次数，输出出现最多的前 n 个词。

  Python 知识点：Counter、lambda、sorted() 的 key 参数
"""
# 练习时要留意：Counter 是 Python 内置的快捷统计工具，遇到类似的统计需求直接用它
import re
from collections import Counter

def word_frequency(text: str) -> dict[str, int]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return dict(Counter(words))

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == "__main__":
    sample = "Hello world! Hello Python. Python is fun, Python is powerful."
    freq = word_frequency(sample)
    print("词频统计:", freq)
    print(f"Top {min(3, len(freq))}:", top_n(freq, 3))
