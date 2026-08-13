from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from backend.models.transaction import Transaction


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
) -> list[Transaction]:
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )



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