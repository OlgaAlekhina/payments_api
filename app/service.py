from pydantic import EmailStr
from sqlalchemy import select
from .models import async_session_maker, User


async def get_user_by_email(email: EmailStr):
	""" Поиск пользователя в БД по email """
	async with async_session_maker() as session:
		query = select(User).filter_by(email=email)
		result = await session.execute(query)
		return result.scalar_one_or_none()


async def get_user_by_id(user_id: int):
	""" Поиск пользователя в БД по id """
	async with async_session_maker() as session:
		query = select(User).filter_by(id=user_id)
		result = await session.execute(query)
		return result.scalar_one_or_none()