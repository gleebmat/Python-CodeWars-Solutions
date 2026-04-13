from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from decimal import Decimal
from sqlalchemy import Numeric


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

    user_id: Mapped[int] = mapped_column(ForeignKey("user_id"), nullable=False)
