from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.dependencies.auth import get_current_user
from backend.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
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
    response_model = list[TransactionResponse],
)
def get_transactions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_transaction(
        db = db,
        user_id = current_user.id,
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
    user_id = 1

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