from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class TransactionCreate(BaseModel):
    category_id: int
    amount: Decimal = Field(gt=0)
    description: str | None = None
    transaction_date: date



class TransactionUpdate(BaseModel):
    category_id: int
    amount: Decimal = Field(gt=0)
    description: str | None = None
    transaction_date: date



class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    description: str | None
    transaction_date: date

    model_config = ConfigDict(from_attributes = True)