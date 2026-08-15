from datetime import date
from decimal import Decimal
from math import ceil

from sqlalchemy.orm import Session

from backend.models.transaction import Transaction
from backend.models.category import Category


def create_transaction(
    db: Session,
    user_id: int,
    category_id: int,
    amount: Decimal,
    description: str | None,
    transaction_date: date,
) -> Transaction:
    transaction = Transaction(
        user_id = user_id,
        category_id = category_id,
        amount = amount,
        description = description,
        transaction_date = transaction_date,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction



def get_transaction(
    db: Session,
    user_id: int,
    page: int,
    limit: int,
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
    transaction_type: str | None = None,
    search: str | None = None,
) -> dict:

    query = (
        db.query(Transaction)
        .join(Category, Category.id == Transaction.category_id)
        .filter(Transaction.user_id == user_id)
    )

    if start_date is not None:
        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    if category_id is not None:
        query = query.filter(
            Transaction.category_id == category_id
        )

    if transaction_type is not None:
        query = query.filter(
            Category.type == transaction_type
        )

    if search is not None:
        query = query.filter(
            Transaction.description.ilike(f"%{search}%")
        )



    total = query.count()

    total_pages = ceil(total / limit) if total > 0 else 0

    offset = (page - 1) * limit

    transactions = (
        query
        .order_by(Transaction.transaction_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


    return {
        "items": transactions,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }



def get_transaction_by_id(
    db: Session,
    user_id: int,
    transaction_id: int,
) -> Transaction | None:
    return (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
        .first()
    )



def update_transaction(
    db: Session,
    user_id: int,
    transaction_id: int,
    category_id: int,
    amount: Decimal,
    description: str | None,
    transaction_date: date,
) -> Transaction | None:
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
        .first()
    )

    if transaction is None:
        return None


    transaction.category_id = category_id
    transaction.amount = amount
    transaction.description = description
    transaction.transaction_date = transaction_date

    db.commit()
    db.refresh(transaction)

    return transaction



def delete_transaction(
    db: Session,
    user_id: int,
    transaction_id: int,
) -> bool:
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
        .first()
    )

    if transaction is None:
        return False

    db.delete(transaction)
    db.commit()

    return True