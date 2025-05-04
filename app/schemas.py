from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=30, description="Пароль длиной 8-30 символов")


class UserData(BaseModel):
    id: int
    email: EmailStr = Field(..., description="Электронная почта")
    full_name: str = Field(..., min_length=1, max_length=30, description="Полное имя длиной 1-30 символов")
