from config.db_conf import get_db
from crud import users
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: AsyncSession = Depends(get_db),
):
    # Bearer xxxxx
    # token = authorization.split(" ")[1]  # Bearer token_value

    token = authorization.replace("Bearer ", "")  # Bearer token_value

    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token或则已经过期的令牌",
        )

    return user
