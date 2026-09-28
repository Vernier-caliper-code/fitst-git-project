from config.db_config import get_db
from crud import users
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data:UserRequest,db: AsyncSession = Depends(get_db)):  # 用户信息 和 db
    #注册逻辑：验证用户是否存在 ->创建用户 ->生成Token ->响应结果
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user= await users.create_user(db,user_data)
    
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": user.id,
                "username": user_data.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }