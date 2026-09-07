from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.category import Category
from backend.models.transaction import Transaction


def get_monthly_summary(
    db: Session,
    user_id: int,
    year: int,
    month: int,
) -> dict[str, Decimal | int]:

    income = (
        db.query(
            func.coalesce(
                func.sum(Transaction.amount),
                0,
            )
        )
        .join(
            Category,
            Category.id == Transaction.category_id,
        )
        .filter(
            Transaction.user_id == user_id,
            Category.type == "income",
            func.extract(
                "year",
                Transaction.transaction_date,
            ) == year,
            func.extract(
                "month",
                Transaction.transaction_date,
            ) == month,
        )
        .scalar()
    )

    expense = (
        db.query(
            func.coalesce(
                func.sum(Transaction.amount),
                0,
            )
        )
        .join(
            Category,
            Category.id == Transaction.category_id,
        )
        .filter(
            Transaction.user_id == user_id,
            Category.type == "expense",
            func.extract(
                "year",
                Transaction.transaction_date,
            ) == year,
            func.extract(
                "month",
                Transaction.transaction_date,
            ) == month,
        )
        .scalar()
    )

    income = Decimal(income)
    expense = Decimal(expense)

    return {
        "year": year,
        "month": month,
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
    }



def get_category_breakdown(
    db: Session,
    user_id: int,
    year: int,
    month: int,
    transaction_type: str,
) -> list[dict]:

    results = (
        db.query(
            Category.id,
            Category.name,
            func.sum(Transaction.amount),
        )
        .join(
            Transaction,
            Transaction.category_id == Category.id,
        )
        .filter(
            Transaction.user_id == user_id,
            Category.type == transaction_type,
            func.extract(
                "year",
                Transaction.transaction_date,
            ) == year,
            func.extract(
                "month",
                Transaction.transaction_date,
            ) == month,
        )
        .group_by(
            Category.id,
            Category.name,
        )
        .order_by(
            func.sum(Transaction.amount).desc()
        )
        .all()
    )

    return [
        {
            "category_id": row.id,
            "category_name": row.name,
            "total_amount": row[2],
        }
        for row in results
    ]



def get_monthly_trend(
    db:  Session,
    user_id: int,
    months: int,
) -> list[dict]:

    results = (
        db.query(
            func.extract(
                "year",
                Transaction.transaction_date,
            ).label("year"),
            func.extract(
                "month",
                Transaction.transaction_date,
            ).label("month"),
            Category.type,
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(
            Category,
            Category.id == Transaction.category_id,
        )
        .filter(
            Transaction.user_id == user_id,
        )
        .group_by(
            func.extract(
                "year",
                Transaction.transaction_date,
            ),
            func.extract(
                "month",
                Transaction.transaction_date,
            ),
            Category.type,
        )
        .order_by(
            func.extract(
                "year",
                Transaction.transaction_date,
            ),
            func.extract(
                "month",
                Transaction.transaction_date,
            ),
        )
        .all()
    )

    monthly_data = {}


    for row in results:
        year = int(row.year)
        month = int(row.month)
        transaction_type = row.type
        total_amount = Decimal(row.total_amount)

        key = (year, month)

        if key not in monthly_data:
            monthly_data[key] = {
                "year": year,
                "month": month,
                "total_income": Decimal("0"),
                "total_expense": Decimal("0"),
            }
            
        if transaction_type == "income":
                monthly_data[key]["total_income"] = total_amount


        elif transaction_type == "expense":
            monthly_data[key]["total_expense"] = total_amount


        return [
            {
                    **data,
                    "balance": data["total_income"] - data["total_expense"],
            }
            for data in monthly_data.values()
        ]
                
            