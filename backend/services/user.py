from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from backend.models.user import User



password_hash = PasswordHash.recommended()



def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
) -> User:
    hashed_password = password_hash.hash(password)

    
    user = User(
        name = name,
        email = email,
        password = hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def get_users(
    db: Session,
) -> list[User]:
    return (
        db.query(User)
        .order_by(User.id.asc())
        .all()
    )



def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def update_user(
    db: Session,
    user_id: int,
    name: str,
    email: str,
) -> User | None:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        return None



    user.name = name
    user.email = email 

    db.commit()
    db.refresh(user)

    return user



def delete_user(
    db: Session,
    user_id: int,
) -> bool:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        return False


    
    db.delete(user)
    db.commit()

    return True