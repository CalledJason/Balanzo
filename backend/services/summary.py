from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.category import Category
from backend.models.transaction import Transaction

def get_summary(
    db: Session,
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
) -> dict[str, Decimal]:

    income_query = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .join(Category, Category.id == Transaction.category_id)
        .filter(
            Transaction.user_id == user_id,
            Category.type == "income",
        )
    )

    expense_query = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .join(Category, Category.id == Transaction.category_id)
        .filter(
            Transaction.user_id == user_id,
            Category.type == "expense",
        )
    )

    if start_date is not None:
        income_query = income_query.filter(
            Transaction.transaction_date >= start_date
        )
        expense_query = expense_query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        income_query = income_query.filter(
            Transaction.transaction_date <= end_date
        )
        expense_query = expense_query.filter(
            Transaction.transaction_date <= end_date
        )




    income = Decimal(income_query.scalar())
    expense = Decimal(expense_query.scalar())

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
    }