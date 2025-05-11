from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from .models import async_session_maker, User


async def get_user_by_email(email: EmailStr):
	""" Получение пользователя из БД по email """
	async with async_session_maker() as session:
		query = select(User).filter_by(email=email)
		result = await session.execute(query)
		return result.scalar_one_or_none()


async def get_user_by_id(user_id: int):
	""" Получение пользователя из БД по id """
	async with async_session_maker() as session:
		query = select(User).filter_by(id=user_id)
		result = await session.execute(query)
		return result.scalar_one_or_none()


async def get_accounts(user_id: int):
	""" Получение счетов пользователя из БД по id """
	async with async_session_maker() as session:
		query = select(User).filter_by(id=user_id)
		result = await session.execute(query)
		user = result.scalar_one_or_none()
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id = {user_id} не найден")
		return user.accounts


async def get_payments(user_id: int):
	""" Получение платежей пользователя из БД по id """
	async with async_session_maker() as session:
		query = select(User).filter_by(id=user_id)
		result = await session.execute(query)
		user = result.scalar_one_or_none()
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id = {user_id} не найден")
		payments = [payment for account in user.accounts for payment in account.payments]
		return payments


async def add_user(email: EmailStr, password: str, full_name: str, is_user: bool):
	""" Добавление нового пользователя в БД """
	async with async_session_maker() as session:
		async with session.begin():
			new_instance = User(email=email, password=password, full_name=full_name, is_user=is_user)
			session.add(new_instance)
			try:
				await session.commit()
			except SQLAlchemyError as e:
				await session.rollback()
				raise e
			return new_instance

