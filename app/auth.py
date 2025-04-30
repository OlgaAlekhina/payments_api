from passlib.context import CryptContext
from pydantic import EmailStr
from .service import find_user
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import get_auth_data

# создаем контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """ Создает хэш пароля """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Сравнивает обычный пароль с хэшем """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    """ Функция для аутентификации пользователя """
    user = await find_user(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def create_access_token(data: dict) -> str:
    """ Функция для для генерации JWT токена """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt
