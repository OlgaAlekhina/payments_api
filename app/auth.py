from passlib.context import CryptContext
from pydantic import EmailStr
from .service import get_user_by_email, get_user_by_id
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import get_auth_data
from fastapi import Request, HTTPException, status, Depends


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
    user = await get_user_by_email(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def create_access_token(data: dict) -> str:
    """ Функция для генерации JWT токена """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def get_token(request: Request):
    """ Функция для получения JWT токена из cookie """
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен авторизации отсутствует')
    return token


async def get_current_user(token: str = Depends(get_token)):
    """ Функция для получения пользователя из JWT токена из cookie """
    # расшифровываем токен
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен имеет неправильный формат')
    # проверяем срок действия токена
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Срок действия токена истек')
    # получаем id пользователя из токена
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='ID пользователя не найден')
    # делаем запрос в БД для получения пользователя
    user = await get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    return user