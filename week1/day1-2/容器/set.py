'''''
集合:内容不重复，数据无序 用{}

不支持下标索引
'''
set1=set()

#添加
set1.add(10)

#删除(两种)
set1.pop()     #这是随机删除
set1.remove(10)   #这是根据元素值进行删除

#清空  set1.clear 

#差集与删除差集
s1={1,34,4}
s2={1,2,6}
s3=s1.difference(s2)   #差集是34，4

set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
set1.difference_update(set2)
print(set1)  # {1, 2, 3}（原集合被修改了！）

#合并集合
s3=s1.union(s2)

#len()




