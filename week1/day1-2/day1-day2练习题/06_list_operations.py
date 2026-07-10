"""
【问题】列表与集合操作
  1. 对 1~20 的偶数求平方，用列表推导式
  2. 用嵌套列表推导式生成 3x3 矩阵
  3. 用列表推导式展平矩阵
  4. 对两个集合求交集、并集、差集

  Python 知识点：列表推导式、嵌套推导式、集合运算
"""
# 列表推导式是 Python 标志性语法，C++ 没有直接对应，要多练几遍
nums = [x**2 for x in range(1, 21) if x % 2 == 0]
print(f"1~20 偶数的平方: {nums}")

matrix = [[i * 3 + j for j in range(3)] for i in range(3)]
print(f"3x3 矩阵: {matrix}")

flatten = [x for row in matrix for x in row]
print(f"展平:       {flatten}")

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"交集: {a & b}  并集: {a | b}  差集: {a - b}")
