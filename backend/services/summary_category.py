from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.category import Category
from backend.models.transaction import Transaction



def get_category_summary(
    db: Session,
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:

    query = (
        db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            Category.type.label("type"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(
            Transaction,
            Transaction.category_id == Category.id,
        )
        .filter(
            Transaction.user_id == user_id,
        )
        .group_by(
            Category.id,
            Category.name,
            Category.type,
        )
        .order_by(Category.id.asc())
    )

    if start_date is not None:
        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    results = query.all()

    return [
        {
            "category_id": row.category_id,
            "category_name": row.category_name,
            "type": row.type,
            "total": Decimal(row.total),
        }
        for row in results
    ]