from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends , HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.income import IncomeCreate
from app.database.mongodb import income_collection
from app.security.jwt import verify_access_token

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)

security = HTTPBearer()


@router.post("/")
def create_income(
    income: IncomeCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    new_income = {
        "user_id": ObjectId(user_id),
        "title": income.title,
        "amount": income.amount,
        "category": income.category,
        "description": income.description,
        "date": income.date,
        "created_at": datetime.now(timezone.utc)
    }

    result = income_collection.insert_one(new_income)

    return {
        "message": "Income added successfully",
        "income_id": str(result.inserted_id)
    }

@router.get("/")
def get_income(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    incomes = list(
        income_collection.find({
            "user_id": ObjectId(user_id)
        })
    )

    for income in incomes:
        income["id"] = str(income.pop("_id"))
        income["user_id"] = str(income["user_id"])

    return incomes


@router.put("/{income_id}")
def update_income(
    income_id: str,
    income: IncomeCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    if not ObjectId.is_valid(income_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid income ID"
        )

    result = income_collection.update_one(
        {
            "_id": ObjectId(income_id),
            "user_id": ObjectId(user_id)
        },
        {
            "$set": {
                "title": income.title,
                "amount": income.amount,
                "category": income.category,
                "description": income.description,
                "date": income.date
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    return {
        "message": "Income updated successfully"
    }

@router.delete("/{income_id}")
def delete_income(
    income_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    if not ObjectId.is_valid(income_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid income ID"
        )

    result = income_collection.delete_one({
        "_id": ObjectId(income_id),
        "user_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    return {
        "message": "Income deleted successfully"
    }