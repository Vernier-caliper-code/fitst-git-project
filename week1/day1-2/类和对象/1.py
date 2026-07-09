
#类内函数一定要带self ，内部可以访问变量
class student2:
    name=None
    def sayhi(self):
        print("hello")
        self.name="dai"  #访问的时候一定要加.self

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

#---------------------------------------------------
#在python里面，保护属性只是一种约定，还是可以访问，但是私有属性是不可以访问的（他的作用机制是，把他重命名了）

class Student:
    def __init__(self, name, score, id_number):
        self.name = name              # 公有
        self._score = score           # 保护
        self.__id_number = id_number  # 私有
    
    def _calc_grade(self):            # 保护方法
        if self._score >= 90:
            return "A"
        elif self._score >= 80:
            return "B"
        else:
            return "C"
    
    def __validate_id(self):          # 私有方法
        return len(self.__id_number) == 18
    
    def get_info(self):               # 公有方法
        valid = "有效" if self.__validate_id() else "无效"
        return f"{self.name}，成绩：{self._score}，身份证：{valid}"

# 使用
s = Student("张三", 85, "110101199001011234")

# 公有：可以访问
print(s.name)          # 张三 ✅

# 保护：可以访问，但不建议
print(s._score)        # 85 ⚠️ 能访问，但应避免

# 私有：不能直接访问
# print(s.__id_number) # ❌ AttributeError

# 但可以通过公有方法
print(s.get_info())    # 张三，成绩：85，身份证：有效






