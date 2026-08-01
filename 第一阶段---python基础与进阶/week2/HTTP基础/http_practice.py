import truststore  #为了保证代码能够运行，github的安全证书之类
import requests
import pandas as pd

truststore.inject_into_ssl()  # 使用 Windows 系统证书库（兼容 Watt Toolkit 的本地证书）

url="https://api.github.com/users/Vernier-caliper-code/repos"

response=requests.get(url,timeout=10)
print(response.status_code)    #响应：看是否请求成功
# print(response.json())

repos=response.json()   #响应：转化为列表            ||||  response.text是str

data=[]
for repo in repos:
    data.append(
        {
            "名称":repo["name"],
            "语言":repo['language'],
            "星标":repo["stargazers_count"],
            "描述":repo.get("description"," "),

        }

    )
df=pd.DataFrame(data)

print("---前5行---")
print(df.head())

print("\n   ====== 语言分布-----")
print(df["语言"].value_counts())

print("\n------星标最多的仓库-----")
print(df.sort_values("星标",ascending=False).head(3))

























