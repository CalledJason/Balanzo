from decimal import Decimal

from pydantic import BaseModel

class CategorySummaryResponse(BaseModel):
    category_id: int
    category_name: str
    type: str
    total: Decimal