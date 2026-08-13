from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.user import UserCreate, UserResponse
from backend.services.user import(
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_users,
)


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

@router.post(
    "/",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED,
)
def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db = db,
        email = user_data.email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already registered",
        )


    user = create_user(
        db = db,
        name = user_data.name,
        email = user_data.email,
        password = user_data.password,
    )

    return user



@router.get(
    "/",
    response_model = list[UserResponse],
)
def get_users_endpoint(
    db: Session = Depends(get_db),
):
    return get_users(db=db)



@router.get(
    "/{user_id}",
    response_model = UserResponse,
)
def get_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(
        db = db,
        user_id = user_id,
    )

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found",
        )

    return user