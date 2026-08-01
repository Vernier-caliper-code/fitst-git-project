'''''

序列支持切片：所以列表、元组、字符串支持切片（从一个序列中取出一个子序列）
[a:b:c]  #a是开始(闭) b是结束(开),c是步长


'''
#正向切片
mylist=[1,2,3,4,5]
temp=mylist[1:4]
print(temp)

#反向切片
text = "Hello World"
# 从索引5开始，向左取到开头
print(text[5::-1])   # ' olleH'
print(text[4::-1])   # 'olleH'
print(text[10::-1])  # 'dlroW olleH'（完全反转）

# 从索引5向左取，到索引2（不包含）
print(text[5:2:-1])  # 'o l'（索引5,4,3）



'''''
数据容器：
max(容器)
len(容器)
min(容器)

sorted(容器)  从小到大排
sorted(容器,reverse=True)  从大到小

'''

lis=[1,2,34,34,3,4,34,3]
print(sorted(lis))

print(max(lis))


#对于列表和元组
#join() 是 Python 中字符串的方法，用于将可迭代对象（如列表、元组）中的元素连接成一个字符串

# 用空格连接
" ".join(["hello", "world"])        # "hello world"

",".join(["a", "b", "c"])            # "a,b,c"

# 用空字符串连接（拼接）
"".join(["py", "thon"])              # "python"

"-".join(["2026", "07", "09"])       # "2026-07-09"
