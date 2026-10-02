from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.recurring import RecurringTransactionCreate
from app.database.mongodb import recurring_collection
from app.security.jwt import verify_access_token

router = APIRouter(
    prefix="/recurring",
    tags=["Recurring Transactions"]
)

security = HTTPBearer()


# CREATE
@router.post("/")
def create_recurring_transaction(
    transaction: RecurringTransactionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = verify_access_token(credentials.credentials)

    if transaction.transaction_type not in ["income", "expense"]:
        raise HTTPException(
            status_code=400,
            detail="transaction_type must be income or expense"
        )

    new_transaction = {
        "user_id": ObjectId(user_id),
        "title": transaction.title,
        "amount": transaction.amount,
        "transaction_type": transaction.transaction_type,
        "category": transaction.category,
        "frequency": transaction.frequency,
        "start_date": transaction.start_date,
        "description": transaction.description,
        "created_at": datetime.now(timezone.utc)
    }

    result = recurring_collection.insert_one(new_transaction)

    return {
        "message": "Recurring transaction created successfully",
        "recurring_id": str(result.inserted_id)
    }


# READ
@router.get("/")
def get_recurring_transactions(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = verify_access_token(credentials.credentials)

    transactions = list(
        recurring_collection.find({
            "user_id": ObjectId(user_id)
        })
    )

    for transaction in transactions:
        transaction["id"] = str(transaction.pop("_id"))
        transaction["user_id"] = str(transaction["user_id"])

    return transactions


# UPDATE
@router.put("/{recurring_id}")
def update_recurring_transaction(
    recurring_id: str,
    transaction: RecurringTransactionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = verify_access_token(credentials.credentials)

    if not ObjectId.is_valid(recurring_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid recurring transaction ID"
        )

    if transaction.transaction_type not in ["income", "expense"]:
        raise HTTPException(
            status_code=400,
            detail="transaction_type must be income or expense"
        )

    result = recurring_collection.update_one(
        {
            "_id": ObjectId(recurring_id),
            "user_id": ObjectId(user_id)
        },
        {
            "$set": {
                "title": transaction.title,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "category": transaction.category,
                "frequency": transaction.frequency,
                "start_date": transaction.start_date,
                "description": transaction.description
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Recurring transaction not found"
        )

    return {
        "message": "Recurring transaction updated successfully"
    }


# DELETE
@router.delete("/{recurring_id}")
def delete_recurring_transaction(
    recurring_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = verify_access_token(credentials.credentials)

    if not ObjectId.is_valid(recurring_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid recurring transaction ID"
        )

    result = recurring_collection.delete_one({
        "_id": ObjectId(recurring_id),
        "user_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Recurring transaction not found"
        )

    return {
        "message": "Recurring transaction deleted successfully"
    }