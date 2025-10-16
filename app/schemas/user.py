'''from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None

    # Pydantic v2: 从 ORM 对象序列化
    model_config = ConfigDict(from_attributes=True)
'''
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None

    class Config:
        orm_mode = True