"""''
目标： Get 请求方法演练

案例：  1.http://www.baidu.com


1.请求：
请求方法：GET

2.响应：
响应对象.url # 获取请求url
响应对象.status_code # 获取响应状态码
响应对象.text # 以文本形式显示响应内容
"""

import requests

url = "http://www.baidu.com"
# 1.获取请求
response = requests.get(url)

# 2.响应
print("请求url:", response.url)  # 获取请求url
print("状态码：", response.status_code)  # 获取响应状态码
print("文本相应内容：",response.text)     # 以文本形式显示响应内容（返回的是字符串）
print("\n")



"""''
目标： Get 请求带参方法演练

案例：     1.http://www.baidu.com?id=1001
         2.http://www.baidu.com?id=1001,1002
         3.http://www.baidu.com?id=1001&kw=北京


1.请求：
    请求方法：GET
参数： 
    params:字典或字符串（推荐使用字典）
2.响应：
响应对象.url # 获取请求url
响应对象.status_code # 获取响应状态码
响应对象.text # 以文本形式显示响应内容
"""

#import requests

url = "http://www.baidu.com"
params1={"id":1001}
params2={"id":"1001,1002"}
params3={"id":1001,"kw":"北京"}
# 1.获取请求
response = requests.get(url,params=params1)   #这里的params自动拼接到url上，网站就是"http://www.baidu.com？id=1001"
# response=requests.get(url,params=params2)  #
# response=requests.get(url,params=params3) 

# 2.响应
print("请求url:", response.url)  # 获取请求url
print("状态码：", response.status_code)  # 获取响应状态码
print("文本相应内容：",response.text)     # 以文本形式显示响应内
