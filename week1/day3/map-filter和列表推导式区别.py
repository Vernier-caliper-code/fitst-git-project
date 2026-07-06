#map  vs  列表推导式

  # map 方式（C++ 思维）
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))

# 列表推导式 ✔ Pythonic
squares = [x**2 for x in nums]

# filter 方式
evens = list(filter(lambda x: x % 2 == 0, nums))

# 列表推导式 ✔
evens = [x for x in nums if x % 2 == 0]

# map + filter 组合（最丑）
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))

# 列表推导式 ✔ Pythonic
squares = [x**2 for x in nums]

# filter 方式
evens = list(filter(lambda x: x % 2 == 0, nums))

# 列表推导式 ✔
evens = [x for x in nums if x % 2 == 0]

# map + filter 组合（最丑）
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))

 # 列表推导式 ✔ 清晰多了
result = [x**2 for x in nums if x % 2 == 0]


