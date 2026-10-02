from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.mongodb import (
    expenses_collection,
    income_collection
)
from app.security.jwt import verify_access_token


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        user_id = verify_access_token(credentials.credentials)
        return ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@router.get("/")
def get_analytics(
    user_id: ObjectId = Depends(get_current_user_id)
):
    expenses = list(
        expenses_collection.find({
            "user_id": user_id
        })
    )

    incomes = list(
        income_collection.find({
            "user_id": user_id
        })
    )

    total_expenses = sum(
        float(expense.get("amount", 0))
        for expense in expenses
    )

    total_income = sum(
        float(income.get("amount", 0))
        for income in incomes
    )

    balance = total_income - total_expenses

    # Category-wise expenses
    category_expenses = {}

    for expense in expenses:
        category = expense.get("category", "Other")
        amount = float(expense.get("amount", 0))

        category_expenses[category] = (
            category_expenses.get(category, 0) + amount
        )

    # Monthly income and expenses
    monthly_data = {}

    for income in incomes:
        date = income.get("date")

        if date:
            month_key = date.strftime("%Y-%m")

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "income": 0,
                    "expenses": 0
                }

            monthly_data[month_key]["income"] += float(
                income.get("amount", 0)
            )

    for expense in expenses:
        date = expense.get("date")

        if date:
            month_key = date.strftime("%Y-%m")

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "income": 0,
                    "expenses": 0
                }

            monthly_data[month_key]["expenses"] += float(
                expense.get("amount", 0)
            )

    # Sort months
    monthly_data = dict(
        sorted(monthly_data.items())
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "category_expenses": category_expenses,
        "monthly_data": monthly_data
    }