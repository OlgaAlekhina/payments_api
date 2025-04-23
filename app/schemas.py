from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=30, description="Пароль длиной 8-30 символов")
