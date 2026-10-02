from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.expense import ExpenseCreate
from app.database.mongodb import expenses_collection
from app.security.jwt import verify_access_token

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

security = HTTPBearer()

#POST
@router.post("/")
def create_expense(
    expense: ExpenseCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    new_expense = {
        "user_id": ObjectId(user_id),
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "date": expense.date,
        "created_at": datetime.now(timezone.utc)
    }

    result = expenses_collection.insert_one(new_expense)

    return {
        "message": "Expense added successfully",
        "expense_id": str(result.inserted_id)
    }

#GET
@router.get("/")
def get_expenses(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    expenses = list(
        expenses_collection.find({
            "user_id": ObjectId(user_id)
        })
    )

    for expense in expenses:
        expense["id"] = str(expense.pop("_id"))
        expense["user_id"] = str(expense["user_id"])

    return expenses

#DELETE
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )

    result = expenses_collection.delete_one({
        "_id": ObjectId(expense_id),
        "user_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }

#UPDATE 
@router.put("/{expense_id}")
def update_expense(
    expense_id: str,
    expense: ExpenseCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )

    result = expenses_collection.update_one(
        {
            "_id": ObjectId(expense_id),
            "user_id": ObjectId(user_id)
        },
        {
            "$set": {
                "title": expense.title,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense updated successfully"
    }