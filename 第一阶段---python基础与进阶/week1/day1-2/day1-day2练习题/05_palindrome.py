"""
【问题】回文检查器
  判断一个字符串是否是回文（正反读一样）。
  要求：忽略大小写、忽略标点符号和空格。
  "A man, a plan, a canal: Panama" -> 是回文
  "race a car" -> 不是回文

  扩展：给定一个单词列表，找出所有是回文的单词。

  Python 知识点：isalnum()、列表推导式过滤、切片[::-1]
"""
def is_palindrome(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]

def find_palindromes(words: list[str]) -> list[str]:
    return [w for w in words if is_palindrome(w)]

if __name__ == "__main__":
    test_cases = ["A man, a plan, a canal: Panama", "race a car", "上海自来水来自海上"]
    for t in test_cases:
        print(f"'{t[:20]}...' -> {'是回文' if is_palindrome(t) else '不是回文'}")

    words = ["level", "hello", "radar", "world", "madam"]
    print(f"列表中的回文: {find_palindromes(words)}")
