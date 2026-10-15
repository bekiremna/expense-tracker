from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class CategoryOut(CategoryIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ExpenseIn(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="CHF", pattern=r"^[A-Z]{3}$")
    spent_at: date
    note: str | None = Field(default=None, max_length=255)
    category_id: int


class ExpenseOut(ExpenseIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoryTotal(BaseModel):
    category: str
    total: Decimal
