
#类内函数一定要带self ，内部可以访问变量
class student2:
    name=None
    def sayhi(self):
        print("hello")
        self.name="dai"

    def say_hi2(self,temp):
        print(f"{temp}")   

stu2=student2()
stu2.say_hi2(2)
stu2.sayhi()


#2.__init__的用法： 初始化 ，在创建类的时候自动调用
class students:
    def __init__(self,name,age,tel):
        self.name=name
        self.__age=age   #私有成员
        self._tel=tel   #保护成员
        print("创建了一个students类")

p1=students("dai",12,23432)
p1.__age=12
print(p1.__age)



#----------------------------------------------------
#3.继承
class student:
    score=None

class student4:
    score=None
    
#单继承
class stu(student,student2):
    score2=None

#多继承
class stu3(student,student2):
    pass  #表示为空

#---------------------------------------------------

#多态见图片





