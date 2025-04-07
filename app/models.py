from typing import List

from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
	pass


class User(Base):
	__tablename__ = "user"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(30), unique=True)
	full_name: Mapped[str] = mapped_column(String(30))
	accounts: Mapped[List["Account"]] = relationship(back_populates="user")


class Account(Base):
	__tablename__ = "account"

	id: Mapped[int] = mapped_column(primary_key=True)
	balance: Mapped[float] = mapped_column(DECIMAL(10, 2))
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
	user: Mapped["User"] = relationship(back_populates="accounts")
	payments: Mapped[List["Payment"]] = relationship(back_populates="account")


class Payment(Base):
	__tablename__ = "payment"

	id: Mapped[int] = mapped_column(primary_key=True)
	amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
	account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
	account: Mapped["Account"] = relationship(back_populates="payments")