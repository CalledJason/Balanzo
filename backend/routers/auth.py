from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.user import UserCreate, UserResponse
from backend.services.auth import authenticate_user
from backend.services.user import create_user, get_user_by_email
from backend.services.security import create_access_token
from backend.dependencies.auth import get_current_user
from backend.models.user import User


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED,
)
def register(
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
            detail = "Email alreaady registered",
        )

    return create_user(
        db = db,
        name = user_data.name,
        email = user_data.email,
        password = user_data.password,
    )



@router.post(
    "/login",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db = db,
        email = form_data.username,
        password = form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password",
        )

    access_token = create_access_token(
        user_id = user.id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



@router.get(
    "/me",
    response_model = UserResponse,
)
def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
):
    return current_user