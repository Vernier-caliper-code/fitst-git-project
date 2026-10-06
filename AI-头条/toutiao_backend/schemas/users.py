from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str


class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """

    nickname: str | None = Field(None, max_length=50, description="昵称")
    avatar: str | None = Field(None, max_length=255, description="头像URL")
    gender: str | None = Field(None, max_length=10, description="性别")
    bio: str | None = Field(None, max_length=500, description="个人简介")


# user_info  定义的类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容,
        from_attributes=True,  # 允许从ORM对象属性中取值
    )


# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(
        ..., min_length=6, alias="newPassword", description="新密码"
    )
