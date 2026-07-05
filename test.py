lst=[]
for i in range(100,1000):
    if i%10==6 and i%3==0 and i%5!=0:
        lst.append(i)

print(f"共有{len(lst)}个")