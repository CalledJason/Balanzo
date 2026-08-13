from sqlalchemy.orm import Session

from backend.models.category import Category


def create_category(
    db: Session,
    name: str,
    category_type: str,
) -> Category:
    category = Category(
        name = name,
        type = category_type,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category



def get_categories(
    db: Session,
) -> list[Category]:
    return (
        db.query(Category)
        .order_by(Category.id.asc())
        .all()
    )



def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )



def update_category(
    db: Session,
    category_id: int,
    name: str,
    category_type: str,
) -> Category | None:
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if category is None:
        return None

    category.name = name
    category.type = category_type

    db.commit()
    db.refresh(category)

    return category



def delete_category(
    db: Session,
    category_id: int,
) -> bool:
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if category is None:
        return False


    db.delete(category)
    db.commit()

    return True
