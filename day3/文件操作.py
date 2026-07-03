#补充：可在模式后加 + 实现读写兼用，如 'r+'（读写）、'w+'（写读，会清空）、'a+'（追加读）。
# 加 'b' 处理二进制文件，如 'rb'、'wb'。



#只写文件，如果没有就创建，有的话就覆盖
with open("dai.txt",'w',encoding="utf-8") as f:
    f.write("代学林大帅哥\n")
    f.write("帅哥\n")

#在文件后面追加，不修改源文件，如果没有，他会自动创建
with open("dai.txt","a",encoding="utf-8") as f:
    f.write("他是猛男")


#只写,  这样的读取方式是最省内存的
with open("dai.txt",'r',encoding="utf-8") as f:
    for line in f:
        print(line.strip())   #.strip在这里消除多余的换行



#其他的read方式了解一下就可以

#.read
with open('dai.txt', 'r', encoding='utf-8') as f:
    content = f.read()          # 一次性读取整个文件到内存
    print(content)

#.readlines
with open('dai.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()   # 返回列表，每行是一个元素（包含换行符）
    for line in lines:
        print(line.strip()) # strip() 去掉换行符