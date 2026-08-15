from fastapi import APIRouter, Depends
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
):
    return get_summary(
        db = db,
        user_id = current_user.id,
    )