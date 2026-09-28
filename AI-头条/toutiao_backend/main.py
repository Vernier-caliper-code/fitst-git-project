from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, users
from utils.exception_handlers import register_exception_handlers

app=FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许的源，开发阶段允许所有源，生产环境需要指定源（http:///127.0.0.1:8000这些叫做源）
    allow_credentials=True,    # 允许携带cookie
    allow_methods=["*"],       # 允许的请求方法
    allow_headers=["*"],       # 允许的请求头
)



#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)

@app.get('/')
async def root():
    return {'message':'hello world'}

