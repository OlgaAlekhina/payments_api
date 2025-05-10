import decimal
from typing import List

from sqlalchemy import String, DECIMAL, ForeignKey, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .config import get_db_url


DATABASE_URL = get_db_url()
# создаем асинхронное подключение к БД, используя драйвер asyncpg
engine = create_async_engine(DATABASE_URL)
# создаем фабрику асинхронных сессий для выполнения транзакций в БД
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
	pass


class User(Base):
	__tablename__ = "user"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(30), unique=True)
	password: Mapped[str]
	full_name: Mapped[str] = mapped_column(String(30))
	accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete", passive_deletes=True,
													 lazy='selectin')
	is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
	is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)


class Account(Base):
	__tablename__ = "account"

	id: Mapped[int] = mapped_column(primary_key=True)
	balance: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
	user: Mapped["User"] = relationship(back_populates="accounts")
	payments: Mapped[List["Payment"]] = relationship(back_populates="account", cascade="all, delete", passive_deletes=True,
													 lazy='selectin')


class Payment(Base):
	__tablename__ = "payment"

	id: Mapped[int] = mapped_column(primary_key=True)
	amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
	account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"))
	account: Mapped["Account"] = relationship(back_populates="payments")
