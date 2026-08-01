from pydantic import BaseModel, Field,field_validator

class Person(BaseModel):
    name:str
    age:int=Field(frozen=True,lt=200)  #后面修改age的值或者超过了200，就会报错
    address:str|None=None
    phones:list[str]=Field(default_factory=list)
    #pydantic是不会共享列表的  但是保险起见，我们用了默认工厂

    #自定义验证函数
    @field_validator("phones") #要验证哪个就传哪个的参数
    @classmethod
    def validate_phones(cls,v:list[str]) ->list[str]:  #这里的两个参数分别是cls，和v
        for n in v:
            if len(n)!=11 or n[0]!="1":
                raise ValueError(f"Invalid phones {n}")
        return v

p=Person(name="123",age=18,address="234",phones=["12332432431"])
print(p)

info={"name":"wang","age":18}
#p=Person(**info)  
#print(p)

