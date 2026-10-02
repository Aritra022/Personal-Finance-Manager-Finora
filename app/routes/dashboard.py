from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.mongodb import (
    expenses_collection,
    income_collection
)
from app.security.jwt import verify_access_token


router = APIRouter(
    prefix="/dashboard-data",
    tags=["Dashboard"]
)

security = HTTPBearer()


@router.get("/")
def get_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = verify_access_token(credentials.credentials)
    user_object_id = ObjectId(user_id)

    # Get all expenses and income for this user
    expenses = list(
        expenses_collection.find({
            "user_id": user_object_id
        })
    )

    incomes = list(
        income_collection.find({
            "user_id": user_object_id
        })
    )

    # Calculate total expenses
    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    # Calculate total income
    total_income = sum(
        income["amount"]
        for income in incomes
    )

    # Calculate balance
    balance = total_income - total_expenses

    # Current month
    now = datetime.now(timezone.utc)

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    # Calculate monthly expenses
    monthly_expenses = sum(
        expense["amount"]
        for expense in expenses
        if month_start <= (
            expense["date"].replace(tzinfo=timezone.utc)
            if expense["date"].tzinfo is None
            else expense["date"]
        ) <= now
    )

    # Calculate monthly income
    monthly_income = sum(
        income["amount"]
        for income in incomes
        if month_start <= (
            income["date"].replace(tzinfo=timezone.utc)
            if income["date"].tzinfo is None
            else income["date"]
        ) <= now
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses
    }