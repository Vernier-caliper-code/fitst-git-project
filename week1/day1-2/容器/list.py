"""
可以存不同的数据类型，支持嵌套

"""
#1.嵌套
mylist=[]
mylist=[[12,34,2,4,54],[1,2,4,5]]
print(mylist[0][1])  #输出34
print(mylist[1][3])  #输出5

#2.进阶
array=[1,2,3,4,5]

temp=array.index(5)  # 5的下标是4    找不到就会报错

array[0]=3   #将1改为3   列表的修改

array.insert(2,100) #在下标为2 的前面插入100

array.append(200)  #在列表的最后加入200
array.extend([23,23,34])  #在列表的最后加入23，23，34 注意不是嵌套

array.pop(2)  #删除下标为2 的元素

array.count(2)   #统计某元素在列表内的数量

length=len(array)   #统计列表中的所有元素  

array.clear()


 
#列表推导式    语法：    [表达式 for 变量 in 可迭代对象]  还有一种格式：[表达式 for 变量 in 可迭代对象  if 语句]

# 例子：生成平方数列表
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


#   2. 用嵌套列表推导式生成 3x3 矩阵
matrix = [[i * 3 + j for j in range(3)] for i in range(3)]
print(f"3x3 矩阵: {matrix}")

#   3. 用列表推导式展平矩阵
flatten = [x for row in matrix for x in row]  #从左到右
print(f"展平:       {flatten}")
