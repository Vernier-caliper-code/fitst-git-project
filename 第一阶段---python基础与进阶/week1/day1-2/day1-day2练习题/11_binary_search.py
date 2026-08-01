"""
【问题】C++ 算法用 Python 重写
  把 C++ 中写过的基础算法用 Python 重新实现一遍：
  1. binary_search() — 在有序数组中查找目标值，返回下标，未找到返回 -1
  2. lower_bound() — 返回第一个 >= target 的位置（对应 C++ std::lower_bound）

  Python 知识点：函数定义、while 循环、类型注解
"""
# 这道题的意义在于：你发现 Python 写算法比 C++ 简洁多少？核心逻辑完全一样，少了多少行？

def binary_search(arr: list[int], target: int) -> int:
    """返回 target 在 arr 中的下标，未找到返回 -1"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def lower_bound(arr: list[int], target: int) -> int:
    """返回第一个 >= target 的位置（C++ std::lower_bound）"""
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


if __name__ == "__main__":
    nums = [3, 7, 11, 18, 23, 34, 45, 56, 67, 78]

    print(f"有序数组: {nums}")

    for t in [23, 7, 78, 100, 3]:
        idx = binary_search(nums, t)
        if idx != -1:
            print(f"  binary_search({t}) → 下标 {idx}, 值 {nums[idx]}")
        else:
            print(f"  binary_search({t}) → 未找到")

    # lower_bound 演示
    print(f"\nlower_bound: 第一个 >= 20 的位置 = {lower_bound(nums, 20)} (值 {nums[lower_bound(nums, 20)]})")
    print(f"lower_bound: 第一个 >= 80 的位置 = {lower_bound(nums, 80)} (越界，返回 len)")
