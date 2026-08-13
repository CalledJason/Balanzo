from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.category import(
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from backend.services.category import(
    create_category,
    delete_category,
    update_category,
    get_categories,
    get_category_by_id,
)


router = APIRouter(
    prefix = "/api/categories",
    tags = ["Categories"],
)

@router.post(
    "/",
    response_model = CategoryResponse,
    status_code = status.HTTP_201_CREATED,
)
def create_category_endpoint(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    category = create_category(
        db = db,
        name = category_data.name,
        category_type = category_data.type,
    )

    return category



@router.get(
    "/{category_id}",
    response_model = CategoryResponse,
)
def get_category_by_id_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = get_category_by_id(
        db = db,
        category_id = category_id,
    )

    if category is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found",
        )

    return category



@router.put(
    "/{category_id}",
    response_model = CategoryResponse,
)
def update_category_endpoint(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = update_category(
        db = db,
        category_id = category_id,
        name = category_data.name,
        category_type = category_data.type,
    )

    if category is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found",
        )

    return category



@router.delete(
    "/{category_id}",
    status_code = status.HTTP_204_NO_CONTENT,
)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_category(
        db = db,
        category_id = category_id,
    )

    if not deleted:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found",
        )

    return None