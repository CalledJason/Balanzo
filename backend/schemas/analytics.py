from decimal import Decimal

from pydantic import BaseModel, Field


class MonthlySummaryResponse(BaseModel):
    year: int
    month: int = Field(ge=1, le=12)
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal



class CategoryBreakdownItem(BaseModel):
    category_id: int
    category_name: str
    total_amount: Decimal



class CategoryBreakdownResponse(BaseModel):
    year: int
    month: int = Field(ge=1, le=12)
    items: list[CategoryBreakdownItem]



class MonthlyTrendItem(BaseModel):
    year: int
    month: int = Field(ge=1, le= 12)
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal



class MonthlyTrendResponse(BaseModel):
    items: list[MonthlyTrendItem]