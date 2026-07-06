'''''
元组一旦定义完成，就不可以修改了

如果里面嵌套了列表，可以修改列表的元素
'''

tur=((1,2,3),(1,3,4))

tur[1][1]  #取 3

tur.index(4)

tur.count(2)

len(tur)



''''
字符串：




'''
str=""
str="hello"
count=str.count("l")
length=len(str)
ind=str.index("llo")
str2=str.replace("he","dai")  #这里是形成新的字符串，因为string是不支持修改的

#很少用的
str.split(" ")
str.strip()

