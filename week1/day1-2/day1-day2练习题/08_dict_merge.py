"""
【问题】字典合并与操作
  给定多个字典，合并成一个。相同键的值用后面的覆盖。
  输出合并后的键列表、值列表，以及按键值对的值排序后的结果。

  Python 知识点：字典 |= 运算符合并、sorted() 自定义 key
"""
# d1 |= d2 是 Python 3.9 的新语法，之前用 d1.update(d2)
def merge_dicts(*dicts: dict) -> dict:
    """合并多个字典，后出现的键覆盖前面的"""
    result: dict = {}
    for d in dicts:
        result |= d  # Python 3.9+: |= 运算符合并
    return result

if __name__ == "__main__":
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    d3 = {"d": 5}

    merged = merge_dicts(d1, d2, d3)
    print(f"合并: {merged}")
    print(f"键列表: {list(merged.keys())}")
    print(f"值列表: {list(merged.values())}")
    print(f"按值排序: {sorted(merged.items(), key=lambda x: x[1])}")
