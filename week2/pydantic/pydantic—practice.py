import json
from datetime import datetime
from typing import Optional, TypeVar
from pydantic import BaseModel, Field, field_validator, ValidationError

T = TypeVar("T", bound=BaseModel)

# ============================================================
# 1. 定义模型 —— 每个字段自带类型校验
# ============================================================
class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$", description="邮箱")
    score: Optional[float] = Field(default=None, ge=0, le=100, description="分数")
    created_at: Optional[datetime] = None
    @field_validator("name")
    @classmethod
    def name_no_whitespace(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("用户名不能为空")
        return v
# ============================================================
# 2. 核心函数 —— JSON 字符串 → Pydantic → 校验
# ============================================================
def parse_and_validate(json_str: str, model: type[T]) -> T:
    """输入 JSON 字符串，返回校验后的 Pydantic 模型实例"""
    try:
        raw = json.loads(json_str)          # Step 1: 字符串 → dict
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 格式错误: {e}") from e

    try:
        return model(**raw)                 # Step 2: dict → 模型（自动校验）
    except ValidationError as e:
        raise ValueError(f"数据校验失败:\n{_format_errors(e)}") from e


def _format_errors(e: ValidationError) -> str:
    """把 Pydantic 校验错误格式化为可读信息"""
    lines = []
    for err in e.errors():
        loc = ".".join(str(x) for x in err["loc"])          
        lines.append(f"  {loc}: {err['msg']}")
    return "\n".join(lines)# ============================================================
# 3. 测试
# ============================================================
if __name__ == "__main__":
    # 正确数据
    ok = '{"name": "游标卡尺先生", "age": 25, "email": "user@test.com", "score": 88}'
    try:
        user = parse_and_validate(ok, User)
        print(f"[OK]   name={user.name}, age={user.age}, "
              f"email={user.email}, score={user.score}")
    except ValueError as e:
        print(f"[FAIL] {e}")    # 错误数据: age 为负, email 格式错, name 为空
    bad = '{"name": "  ", "age": -5, "email": "not-an-email"}'
    try:
        parse_and_validate(bad, User)
    except ValueError as e:
        print(f"\n[FAIL] 多条错误一起报告:\n{e}")    # JSON 语法错误
    broken = '{"name": '
    try:
        parse_and_validate(broken, User)
    except ValueError as e:
        print(f"\n[FAIL] JSON 语法错: {e}")