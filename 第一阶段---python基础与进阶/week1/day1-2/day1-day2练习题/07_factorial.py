"""
【问题】阶乘计算
  分别用递归和迭代计算 n!，输出 0! 到 10! 的结果对比。

  Python 知识点：递归函数写法、f-string 对齐格式 :>6
"""
# 和 C++ 几乎一样，重点感受 Python 函数定义的简洁
def factorial_rec(n: int) -> int:
    return 1 if n <= 1 else n * factorial_rec(n - 1)

def factorial_iter(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    for n in range(0, 11):
        print(f"{n:>2}! = {factorial_rec(n):>6} (递归)  {factorial_iter(n):>6} (迭代)")
