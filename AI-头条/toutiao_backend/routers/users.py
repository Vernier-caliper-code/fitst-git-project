from config.db_config import get_db
from crud import users
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
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


