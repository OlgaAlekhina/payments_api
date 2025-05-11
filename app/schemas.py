from typing import List

from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal


class UserAuth(BaseModel):
    """ Модель для авторизации пользователей """
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=30, description="Пароль длиной 8-30 символов")


class UserData(BaseModel):
    """ Модель для получения личных данных пользователей """
    id: int
    email: EmailStr = Field(..., description="Электронная почта")
    full_name: str = Field(..., min_length=1, max_length=30, description="Полное имя длиной 1-30 символов")


class AccountData(BaseModel):
    """ Модель для получения информации о счете """
    id: str
    balance: Decimal = Field(..., description="Баланс счета")


class UserAccounts(BaseModel):
    """ Модель для получения счетов пользователей """
    accounts: List[AccountData]


class PaymentData(BaseModel):
    """ Модель для получения информации о платеже """
    payment_id: int
    account_id: str
    amount: Decimal = Field(..., description="Сумма платежа")


class UserPayments(BaseModel):
    """ Модель для получения платежей пользователей """
    payments: List[PaymentData]
