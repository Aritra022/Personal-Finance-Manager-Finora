from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from bson import ObjectId

from app.database.mongodb import (
    expenses_collection,
    income_collection,
    budgets_collection,
    goals_collection
)

from app.security.jwt import verify_access_token
from app.services.ai_service import ask_finora_ai


router = APIRouter(
    prefix="/ai",
    tags=["Finora AI"]
)

oauth2_scheme = HTTPBearer()


class AIChatRequest(BaseModel):
    question: str


@router.post("/chat")
def ai_chat(
    request: AIChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    token = credentials.credentials

    user_id = verify_access_token(token)

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID"
        )

    user_object_id = ObjectId(user_id)

    # Get user's expenses
    expenses = list(
        expenses_collection.find(
            {"user_id": user_object_id}
        )
    )

    # Get user's income
    income = list(
        income_collection.find(
            {"user_id": user_object_id}
        )
    )

    # Get user's budgets
    budgets = list(
        budgets_collection.find(
            {"user_id": user_object_id}
        )
    )

    # Get user's goals
    goals = list(
        goals_collection.find(
            {"user_id": user_object_id}
        )
    )

    financial_context = f"""
EXPENSES:
{[
    {
        "title": item.get("title"),
        "amount": item.get("amount"),
        "category": item.get("category"),
        "date": str(item.get("date"))
    }
    for item in expenses
]}

INCOME:
{[
    {
        "title": item.get("title"),
        "amount": item.get("amount"),
        "category": item.get("category"),
        "date": str(item.get("date"))
    }
    for item in income
]}

BUDGETS:
{[
    {
        "category": item.get("category"),
        "monthly_limit": item.get("monthly_limit"),
        "month": str(item.get("month"))
    }
    for item in budgets
]}

SAVINGS GOALS:
{[
    {
        "name": item.get("name"),
        "target_amount": item.get("target_amount"),
        "current_amount": item.get("current_amount"),
        "target_date": str(item.get("target_date"))
    }
    for item in goals
]}
"""

    try:
        answer = ask_finora_ai(
            question=request.question,
            financial_context=financial_context
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        print("Gemini error:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to get a response from Finora AI."
        )