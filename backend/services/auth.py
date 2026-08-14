from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from backend.models.user import User
from backend.services.user import get_user_by_email

password_hash = PasswordHash.recommended()



def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = get_user_by_email(
        db = db,
        email = email,
    )

    if user is None:
        return None


    if not password_hash.verify(
        password, 
        user.password,
    ):
        return None


    return user