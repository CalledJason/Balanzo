from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies.auth import get_current_user
from backend.models.user import User

from backend.schemas.analytics import (
    MonthlySummaryResponse,
    CategoryBreakdownResponse,
    MonthlyTrendResponse,
)

from backend.services.analytics import (
    get_monthly_summary,
    get_category_breakdown,
    get_monthly_trend,
)


router = APIRouter(
    prefix = "/api/analytics",
    tags = ["Analytics"],
)


@router.get(
    "/monthly",
    response_model = MonthlySummaryResponse,
)
def get_monthly_summary_endpoint(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_monthly_summary(
        db = db,
        user_id = current_user.id,
        year = year,
        month = month,
    )



@router.get(
    "/categories",
    response_model = CategoryBreakdownResponse,
)
def get_category_breakdown_endpoint(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    transaction_type: str = "expense",
):
    if transaction_type not in {"income", "expense"}:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "transaction_type must be either income or expense",
        )


    items = get_category_breakdown(
        db = db,
        user_id = current_user.id,
        year = year,
        month = month,
        transaction_type = transaction_type,
    )

    return {
        "year": year,
        "month": month,
        "items": items,
    }



@router.get(
    "/trend",
    response_model = MonthlyTrendResponse,
)
def get_monthly_trend_endpoint(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if months < 1 or months > 12:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "months must be between 1 and 12",
        )

    items = get_monthly_trend(
        db = db,
        user_id = current_user.id,
        months = months,
    )

    return {
        "items": items,
    }