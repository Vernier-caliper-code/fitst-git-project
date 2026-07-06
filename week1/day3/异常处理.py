try:
    with open("di.txt","r",encoding="utf-8") as f:
        for line in f:
            print(line.strip())

#如果出现异常执行的语句
except Exception as e:
    print(e)

#如果没有出现异常执行的语句
else:
    print("没有出现异常")

#不管有没有异常，都会执行的语句
finally:
    print("你已经掌握了这个知识点")    


