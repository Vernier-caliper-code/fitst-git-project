'''
json字符串转化为python对象
python对象转化为json字符串
'''

import json

#重要  python对象转化为json字符串
person={"name":"json","age":20,"gender":"male","tel":["123456789","987654321"],"address":{"province":"Guangdong","city":"Shenzhen"}}
jsonstr=json.dumps(person,indent=4,sort_keys=True,ensure_ascii=False)
print(jsonstr)


with open("person.json","w",encoding="utf-8") as f:
    json.dump(person,f,indent=4,sort_keys=True,ensure_ascii=False)
#第二种写法 ：json.dump(person,open("person.json","w",encoding="utf-8"),indent=4,sort_keys=True,ensure_ascii=False)

    



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#注意在读jsonobj的时候，不管是loads还是load，都不能传多余的参数，否则会报错

#json字符串转化为python对象
person2='{"name":"json","age":20,"gender":"male","tel":["123456789","987654321"],"address":{"province":"Guangdong","city":"Shenzhen"}}'
personobj=json.loads(s=person2)
print(personobj)



#重要
with open("person.json","r",encoding="utf-8") as f:
    personobj2=json.load(f)
    print(personobj2)

# person3=json.load(open("person.json","r",encoding="utf-8"))
# print(person3)

