#一.函数的多返回值：有多少个返回值就用多少个变量来接收
def test():
    return 1,3,4

x,y,z=test()   


#---------------------------------------------------------------------------------

#二.函数的多种参数使用方式
#1.位置传参

#2.关键字参数："键=值" 顺序可以不同
def test(name,age):
    return None

test(age=20,name="代")

#3.省参数（默认参数）：在函数的最后，   当没有传递相应的参数时，就会使用默认参数的值
def test(name,age,gender="男"):
    return None

test("tom",20)  #这里的缺了参数，所以默认是男

#---------------------------------------------------------------------------------
#三、不定长参数（可变参数） 用于不确定有多少个参数        两种：位置传递和关键字传递

def demo(*args, **kwargs):      #arguments    keywords arguments
    print(f"args: {args}")      # 元组   (位置传递)
    print(f"kwargs: {kwargs}")  # 字典    （关键字传递）

demo(1, 2, 3, name='Alice', age=25)
# 输出：
# args: (1, 2, 3)
# kwargs: {'name': 'Alice', 'age': 25}

#---------------------------------------------------------------------------------
#四、函数作为参数传递
def test(compute):
    result=compute(1,2)
    print(result)
    
def compute(x,y):
    return x+y

#---------------------------------------------------------------------------------
#五、lambda 匿名函数    没有函数名 只有一个执行语句
def test(compute):
    result=compute(1,2)
    print(result)

test(lambda x,y: x+y)


 #---------------------------------------------------------------------------------
 #六、类型注解

#1.变量
val:int=10

#2.函数
def func(data:int|str|float)   ->int:
    return data