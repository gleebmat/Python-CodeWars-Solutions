from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto

from pydantic import BaseModel


class CurrencyEnum(StrEnum):
    RUB = auto()
    USD = auto()
    EUR = auto()


class OperationType(StrEnum):
    EXPENSE = auto()
    INCOME = auto()
    TRANSFER = auto()


class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None
    subcategory: str | None
    created_at: datetime
