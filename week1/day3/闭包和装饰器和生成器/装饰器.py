#装饰器：（本质就是一个闭包） ：不改变原函数的结构，给原函数增加新功能
#作用：在修改原函数的前提下，给他增加功能

def check_login(fun_name):   
    def fun_inner():              #嵌套
        print("登录中")            #添加功能
        fun_name()                #引用
    return fun_inner                #返回



def comment():
    print("发表评论")


#1.这是传统的方法，手动调用
comment=check_login(comment)    
comment()

print("-" *23)


#2.语法糖： 在要装饰的函数上，直接@装饰器的名字，之后直接调用函数即可
@check_login
def payment():
    print("充值中.....")

payment()
