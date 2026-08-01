import csv


with open ("dai.csv","w",encoding="utf-8",newline='') as f:
    writer=csv.writer(f)
    writer.writerow(["姓名","语文","数学","英语"])
    writer.writerow(["daixuelin",12,234,234])
    writer.writerow(["渣男",324,324,34])

with open("dai.csv","r",encoding="utf-8") as f:
    read=csv.reader(f)
    for row in read:
        print(row)