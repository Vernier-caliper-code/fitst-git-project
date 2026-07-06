"""""
key值不能重复

"""
my_dict={}
my_dict={"周杰伦":99,"林俊杰":12,"代学林":77,"无极":324}

#获取元素
num=my_dict["代学林"]
print(num)

#更新或则添加元素
my_dict["美女"]=13
print(my_dict)

#删除固定的值
my_dict.pop("美女")


#清空  clear   获取个数len


#获取全部的key   以及遍历dict
keys=my_dict.keys()
for e in my_dict:
    print(e)
    print(my_dict[e])


for i  in keys:
    print(i)
    print(my_dict[i])




# 字典的 in 检查的是"键"是否存在
count = {"apple": 3, "banana": 2, "orange": 1}

print("apple" in count)    # True（检查键）
print("banana" in count)   # True（检查键）
print("grape" in count)    # False（键不存在）
print(3 in count)          # False（检查的是键，不是值！）



