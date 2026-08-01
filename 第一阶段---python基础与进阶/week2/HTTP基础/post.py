import requests

url = "http://127.0.0.1:8000/api/departments/"

# 请求 json
data = {
        "data": 
                [{
                "dep_id": "T01",
                "dep_name": "Test学院",
                "master_name": "Test-Master",
                "slogan": "Here is Slogan"
                 } ]
}

response=requests.post(url, json=data)   #这里网站就不是直接拼接到url上了，而是放在了body里面
#这里的data是字典，但是可以自动转化为json格式
#注意这里：post可以传(data,json) 两种参数，data是字典，json是字符串

print(response.json())  #返回类型是字典，可以通过键名来获取响应的值
print(response.text)  #返回类型是字符串，不可以...
print(response.status_code)


