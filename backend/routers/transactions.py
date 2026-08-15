from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.dependencies.auth import get_current_user
from backend.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionPaginatedResponse,
)

from backend.services.transaction import (
    create_transaction,
    get_transaction,
    get_transaction_by_id,
    update_transaction,
    delete_transaction,
)

router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"],
)

@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction_endpoint(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = create_transaction(
        db = db,
        user_id = current_user.id,
        category_id = transaction_data.category_id,
        amount = transaction_data.amount,
        description = transaction_data.description,
        transaction_date = transaction_data.transaction_date,
    )

    return transaction



@router.get(
    "/",
    response_model = TransactionPaginatedResponse,
)
def get_transactions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
    transaction_type: str | None = None,
    search: str | None = None,
):
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "start_date must be before or equal to end_date",
            )



    if page < 1:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "page must be greater than or equal to 1",
        )




    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "limit must be between 1 and 100",
        )



    if transaction_type is not None:
        if transaction_type not in {"income", "expense"}:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "transaction_type must be either income or expense",
            )




    return get_transaction(
        db = db,
        user_id = current_user.id,
        start_date = start_date,
        end_date = end_date,
        category_id = category_id,
        page = page,
        limit = limit,
        transaction_type = transaction_type,
        search = search,
    )



@router.get(
    "/{transaction_id}",
    response_model = TransactionResponse,
)
def get_transaction_by_id_endpoint(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = get_transaction_by_id(
        db = db,
        user_id = current_user.id,
        transaction_id = transaction_id,
    )

    if transaction is None:
        
        raise HTTPException(
            status_code = 404,
            detail = "Transaction not found",
        )

    return transaction



@router.put(
    "/{transaction_id}",
    response_model = TransactionResponse
)
def update_transaction_endpoint(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = update_transaction(
        db = db,
        user_id = current_user.id,
        transaction_id = transaction_id,
        category_id = transaction_data.category_id,
        amount = transaction_data.amount,
        description = transaction_data.description,
        transaction_date = transaction_data.transaction_date,
    )

    if transaction is None:
        raise HTTPException(
            status_code = 404,
            detail="Transaction not found",
        )

    return transaction



@router.delete(
    "/{transaction_id}",
    status_code = status.HTTP_204_NO_CONTENT,
)
def delete_transaction_endpoint(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_transaction(
        db = db,
        user_id = current_user.id,
        transaction_id = transaction_id,
    )

    if not deleted:
        raise HTTPException(
            status_code = 404,
            detail = "Transaction not Found",
        )

    return None