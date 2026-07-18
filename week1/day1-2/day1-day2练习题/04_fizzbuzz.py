"""
【问题】FizzBuzz
  从 1 数到 n：
  - 是 3 的倍数 -> 输出 "Fizz"
  - 是 5 的倍数 -> 输出 "Buzz"
  - 同时是 3 和 5 的倍数 -> 输出 "FizzBuzz"
  - 否则输出数字本身

  Python 知识点：if/elif/else、f-string 格式化
"""
# 这题练的是 Python 缩进流程控制 + f-string 的 :>3 对齐写法
def fizzbuzz(n: int) -> None:
    for i in range(1, n + 1):
        if i % 15 == 0:
            val = "FizzBuzz"
        elif i % 3 == 0:
            val = "Fizz"
        elif i % 5 == 0:
            val = "Buzz"
        else:
            val = str(i)
        print(f"{i:>3} -> {val}")

if __name__ == "__main__":
    fizzbuzz(30)


