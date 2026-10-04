from config.db_conf import get_db
from crud import users
from fastapi import APIRouter, Depends, HTTPException
from models.users import User
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data:UserRequest,db: AsyncSession = Depends(get_db)):  # 用户信息 和 db
    #注册逻辑：验证用户是否存在 ->创建用户 ->生成Token ->响应结果
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user= await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)

    #因为这里的代码结构高度的重复，所以说我们直接封装成一个函数
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user_data.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }

    response_data = UserAuthResponse(
        token=token,
        userInfo=UserInfoResponse.model_validate(user),
    )
    return success_response(message="注册成功",data=response_data)


@router.post("/login")
async def login(user_data:UserRequest,db: AsyncSession = Depends(get_db)):
    #登录逻辑；验证用户是否存在 ->验证密码 ->生成Token ->响应结果
    user=await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token=await users.create_token(db,user.id)
    response_data = UserAuthResponse(
        token=token,
        userInfo=UserInfoResponse.model_validate(user),
    )
    return success_response(message="登录成功",data=response_data)




#查Token查用户 -> 封装crud -> 功能整合成一个工具函数 —>路由读入使用: 依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
     return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))