#1.这是我的第一个python程序
c=3
"""
2.
这是多行注释


"""

#3.
day="monday"
print("今天星期","day","哦")

#4
a=10.3
a=int(a)  #注意这里一定要用一个变量来接受，int(a)不修改原变量的值
print(a)

#5
a=20
b=2
temp=a/b
print(temp)  #输出10.0  /是小数除法

temp=a//b
print(temp)  #输出10.0  //是整数除法


# 6基本用法：保留指定位数小数
a = 10.34567
print("%.2f" %a)       #10.35

#7字符串拼接
str="代学林"
print(str+"大帅哥")


#8字符串的格式化
name="代"
year=2005
price=123.32
message=f"{name},成立于:{year},价格是{price}"
print(message)
print(f"{name}成立于：{year},价格是：{price}")
print(f"{name}成立于,{year},{price}是无价的")

print("%s成立与:%d,价格是：%f"%(name,year,price))  #格式化第二种方法


#9.输入   注意了：无论输入的什么类型，获得到的数据永远都是字符串类型
print("你的名字是：")
name=input()
print(type(name))  #输出<class  str>

name=input("你的名字是：")  #这两个是等价的

#-----------------------------------------------------------------------
#1.if elif else
a=10
b=20
c=30

if a>b:
    print("Win")
elif c>b:
    print("WIN")
else:
    print("nowin")

#2.while
i=0
while i>100:
    print("代学林大帅哥")
    i+=1 #注意python里面没有++运算符

#3.for

name="itheima"
for x in name:
    print(x)    

#注意了这里的x是临时变量

for z in range(5): #左闭右开
    print(z)

for z in  range(5,10):
    print(z)

for z in range(5,10,2):  #这里的参数依次是start  end   步长
    print(z)    #输出5 7 9   


def func(a):
    return True



