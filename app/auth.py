from passlib.context import CryptContext

# создаем контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """ Создает хэш пароля """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Сравнивает обычный пароль с хэшем """
    return pwd_context.verify(plain_password, hashed_password)