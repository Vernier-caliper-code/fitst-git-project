def fun_outer():
    a=100
    def fun_inner():                  #嵌套
        nonlocal a  #是用nonlocal关键字，是内部函数能够改变外部变量的值
        a=a+1                         #引用（这里直接对a进行修改）
        print(f"a的结果是{a}")
    return fun_inner                    #返回

if __name__=='__main__':
    fun_inner=fun_outer()
    fun_inner()
    fun_inner()
    fun_inner() 

"""""
运行方式	                    __name__ 的值
直接运行该 Python 文件	        '__main__'
被其他文件导入（import）	    模块的文件名（不含 .py 后缀）

为什么要这样设计？
1. 双重用途
一个 Python 文件既可以作为脚本直接运行，也可以作为模块被导入。这个结构让代码能同时支持两种场景。

2. 防止意外执行
如果不加这个判断，导入模块时会自动执行所有顶层代码，可能不是你想要的结果

"""


"""
总体代码解释：

这段代码展示了 Python 中的闭包（Closure）特性，核心机制是：

外部函数 fun_outer() 定义了局部变量 a = 100

内部函数 fun_inner() 使用 nonlocal a 声明，表明要修改的是外部函数作用域中的 a，而不是创建新的局部变量

fun_outer() 返回 fun_inner 函数对象（注意是返回函数本身，不是调用它）

在 main 中：

fun_inner = fun_outer() → 执行外部函数，创建并返回内部函数，此时 a 被"记住"（闭包）

连续三次调用 fun_inner() → 每次都会修改并打印同一个 a 变量

"""