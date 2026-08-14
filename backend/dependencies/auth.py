import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session


from backend.database import get_db
from backend.models.user import User
from backend.services.user import get_user_by_id
from backend.services.security import SECRET_KEY, ALGORITHM



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "could not validate credentials",
        headers = {
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)


    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = get_user_by_id(
        db = db,
        user_id = user_id,
    )

    if user is None:
        raise credentials_exception

    return user