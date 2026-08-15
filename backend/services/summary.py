from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.category import Category
from backend.models.transaction import Transaction

def get_summary(
    db: Session,
    user_id: int,
) -> dict[str, Decimal]:

    income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .join(Category, Category.id == Transaction.category_id)
        .filter(
            Transaction.user_id == user_id,
            Category.type == "income",
        )
        .scalar()
    )

    expense = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .join(Category, Category.id == Transaction.category_id)
        .filter(
            Transaction.user_id == user_id,
            Category.type == "expense",
        )
        .scalar()
    )

    income = Decimal(income)
    expense = Decimal(expense)

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
    }