from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies.auth import get_current_user
from backend.schemas.summary import SummaryResponse
from backend.services.summary import get_summary


router = APIRouter(
    prefix = "/api/summary",
    tags = ["Summary"],
)


@router.get(
    "/",
    response_model = SummaryResponse,
)
def get_summary_endpoint(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    start_date: date | None = None,
    end_date: date | None = None,
):
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "start_date must be before or equal to end_date",
            )

    return get_summary(
        db = db,
        user_id = current_user.id,
        start_date = start_date,
        end_date = end_date,
    )