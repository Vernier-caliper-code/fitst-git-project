import pandas as pd  

df=pd.DataFrame(
    {
    "name": ["张三", "李四", "王五", "赵六", "钱七"],
    "age": [20, 22, None, 17, 23],           # None 就是缺失值
    "score": [85, 90, 78, 92, None],
    "city": ["北京", "上海", "北京", "广州", "上海"]
    },index=[1,2,3,4,5]
)


# print(df.head())
# print(df.info())
# print(df.describe())
# print(df.shape)

print(df.isnull())
print(df.groupby("city")["score"].mean())

print(df["score"].apply(lambda x:x**2))


