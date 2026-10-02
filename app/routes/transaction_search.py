
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database.mongodb import (
    expenses_collection,
    income_collection
)
from app.security.jwt import verify_access_token

router = APIRouter(
    prefix="/transactions",
    tags=["Transaction Search"]
)


def search_transactions(
    collection,
    user_id,
    category,
    start_date,
    end_date,
    min_amount,
    max_amount
):
    query = {"user_id": user_id}

    if category:
        query["category"] = {
            "$regex": category,
            "$options": "i"
        }

    if start_date or end_date:
        date_filter = {}

        if start_date:
            date_filter["$gte"] = start_date

        if end_date:
            date_filter["$lte"] = end_date

        query["date"] = date_filter

    if min_amount is not None or max_amount is not None:
        amount_filter = {}

        if min_amount is not None:
            amount_filter["$gte"] = min_amount

        if max_amount is not None:
            amount_filter["$lte"] = max_amount

        query["amount"] = amount_filter

    transactions = list(collection.find(query))

    for transaction in transactions:
        transaction["_id"] = str(transaction["_id"])
        transaction["user_id"] = str(transaction["user_id"])

    return transactions


@router.get("/expenses")
def search_expenses(
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    if min_amount is not None and min_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot be negative"
        )

    if max_amount is not None and max_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum amount cannot be negative"
        )

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot exceed maximum amount"
        )

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    user_id = ObjectId(current_user)

    results = search_transactions(
        expenses_collection,
        user_id,
        category,
        start_date,
        end_date,
        min_amount,
        max_amount
    )

    return {
        "message": "Expenses retrieved successfully",
        "total": len(results),
        "expenses": results
    }


@router.get("/income")
def search_income(
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    if min_amount is not None and min_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot be negative"
        )

    if max_amount is not None and max_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum amount cannot be negative"
        )

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot exceed maximum amount"
        )

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    user_id = ObjectId(current_user)

    results = search_transactions(
        income_collection,
        user_id,
        category,
        start_date,
        end_date,
        min_amount,
        max_amount
    )

    return {
        "message": "Income retrieved successfully",
        "total": len(results),
        "income": results
    }