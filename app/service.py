from pydantic import EmailStr
from sqlalchemy import select
from .models import async_session_maker, User


async def find_user(email: EmailStr):
	""" Ищет пользователя по email в БД """
	async with async_session_maker() as session:
		query = select(User).filter_by(email=email)
		result = await session.execute(query)
		return result.scalar_one_or_none()