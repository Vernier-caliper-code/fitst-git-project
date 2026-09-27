""""
执行： uvicorn 文件名：对象 --reload

1.
get :查询参数（Query)、路径参数(Path)
post: 请求体参数

返回的类型：HTML,自定义

2.异常响应处理

3.中间件：为每个请求添加统一的处理逻辑（记录日志、身份认证、跨域、设置响应头、性能监控等）
 执行顺序，自下而上

4.依赖项注入：
    解决重复性的代码，他就相当于一个组件
"""





from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

app=FastAPI()

#root 
@app.get("/")
async def root():
    return {"message":"ni hao "}

# 路径参数  这里的类型注解是Path
@app.get("/youbiaokachi/{id}")
async def shuaige(id:int=Path(...,gt=0,lt=6,descriptions="书籍的id是从1到5")):
    id_list=[1,2,3,4,5]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="id不存在")

    return {"handsomeboys":id}


#查询参数  这里的类型注解是Query
@app.get("/youbiokachi")
async def get_youbiokachi(skip:int=Query(10, ge=0), limit:int=Query(10, ge=0)):
    return {"skip":skip,"limit":limit}

#需求:设计接口新增图书，图书信息包含:书名、作者、出版社、售价
# 请求体参数  这里的类型注解是Body  用来创建和更行资源
class libary(BaseModel):
    name:str = Field(...,min_length=1,max_length=20)
    author:str = Field(...,min_length=1,max_length=20)
    press:str = Field(...,min_length=1,max_length=20)
    price:float = Field(...,gt=0)

# 请求体
@app.post("/libary")
async def add_libary(libary:libary):
    return libary

# 响应返回HTML
@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<html><body><h1>Hello World</h1></body></html>"


# 响应返回文件格式
@app.get("/file")
async def get_file():
    file_path="./files/1.jpeg"
    return FileResponse(file_path)


# 自定义响应类型  response_model 这个参数用来自定义响应的数据结构
# 对反应的内容进行封装
class CustomResponse(BaseModel):
    code:int = Field(200,description="状态码")
    msg:str = Field("成功",description="状态信息")


@app.get("/duli",response_model=CustomResponse)
async def get_duili(code:int,msg:str):
    return {"code":code,"msg":msg}


""""
中间件的主要作用
1. 统一处理所有请求
   不需要在每个接口中重复写。
2. 记录请求前后信息
   例如耗时、访问日志、请求 ID、调用链路。
3. 修改请求或响应
   可以读取请求信息，也可以修改响应头、Cookie 和响应内容。
4. 实现全局控制
   例如限流、跨域、HTTPS 重定向、压缩响应、统一拒绝非法请求。
5. 处理横切关注点
   与具体业务无关，但大量接口都需要的逻辑。
"""
# 中间件( 执行顺序 自下而上) 
@app.middleware("http")
async def middleware1(request,call_next):
    print("中间件1  start")
    response=await call_next(request)
    print("中间件1  end")
    return response

@app.middleware("http")
async def middleware2(request,call_next):
    print("中间件2  start")
    response=await call_next(request)
    print("中间件2  end")
    return response



#  依赖注入（依赖注入不是单纯复用函数，而是让 FastAPI 根据接口声明，自动准备并注入函数、参数或请求级资源。）
async def common_parameters(
        skip:int=Query(0,ge=0),
        limit:int=Query(60,le=60)

):

    return {"skip":skip,"limit":limit}

@app.get("/items/")
async def read_items(
    common: dict = Depends(common_parameters),
):
    return common