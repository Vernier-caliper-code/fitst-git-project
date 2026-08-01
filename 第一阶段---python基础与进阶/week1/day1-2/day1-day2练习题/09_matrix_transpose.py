"""
【问题】矩阵转置与乘法
  1. 给定一个矩阵，输出它的转置
  2. 用列表推导式实现矩阵乘法 A(3×2) × B(2×4)

  Python 知识点：zip(*matrix) 转置技巧、嵌套列表推导式
"""
# zip(*matrix) 是纯 Python 技巧，解开看：zip([1,2,3], [4,5,6]) -> (1,4),(2,5),(3,6)
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]

def print_matrix(m: list[list[int]], label: str = "") -> None:
    if label:
        print(label)
    for row in m:
        print("  ", row)

if __name__ == "__main__":
    mat = [[1, 2, 3], [4, 5, 6]]
    print_matrix(mat, "原始矩阵:")
    print_matrix(transpose(mat), "转置后:")

    # 列表推导式对比 C++ 的嵌套循环
    print("\n列表推导式矩阵乘法 3x2 × 2x4:")
    A = [[1, 2], [3, 4], [5, 6]]
    B = [[7, 8, 9, 10], [11, 12, 13, 14]]
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B)))
               for j in range(len(B[0]))] for i in range(len(A))]
    for row in result:
        print("  ", row)
