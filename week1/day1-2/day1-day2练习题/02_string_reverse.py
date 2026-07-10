"""
【问题】字符串反转
  输入一段文字，用三种方式反转：
  1. 切片反转：整个字符串倒序
  2. 循环反转：逐个字符反转
  3. 单词反转：按空格拆分，单词顺序倒序，每个单词本身不变
     "hello world" -> "world hello"

  Python 知识点：切片[::-1]、split()、join()
"""
def reverse_slice(s: str) -> str:
    return s[::-1]

def reverse_loop(s: str) -> str:
    result = ""
    for ch in s:
        result = ch + result
    return result

def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])

if __name__ == "__main__":
    text = input("输入一段文字: ")
    print(f"切片反转:   {reverse_slice(text)}")
    print(f"循环反转:   {reverse_loop(text)}")
    print(f"单词反转:   {reverse_words(text)}")
