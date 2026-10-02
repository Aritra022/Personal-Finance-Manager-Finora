
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database.mongodb import budgets_collection, expenses_collection
from app.security.jwt import verify_access_token

router = APIRouter(
    prefix="/budget-tracking",
    tags=["Budget Tracking"]
)


@router.get("/")
def get_budget_tracking(
    current_user: dict = Depends(verify_access_token)
):
    user_id = current_user

    if not user_id or not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    user_id = ObjectId(user_id)

    budgets = list(
        budgets_collection.find({"user_id": user_id})
    )

    results = []

    for budget in budgets:
        category = budget.get("category")
        month = budget.get("month")
        budget_amount = float(budget.get("amount", 0))

        if not isinstance(month, datetime):
            continue

        if month.tzinfo is None:
            month = month.replace(tzinfo=timezone.utc)

        month_start = datetime(
            month.year,
            month.month,
            1,
            tzinfo=timezone.utc
        )

        if month.month == 12:
            next_month = datetime(
                month.year + 1, 1, 1,
                tzinfo=timezone.utc
            )
        else:
            next_month = datetime(
                month.year,
                month.month + 1,
                1,
                tzinfo=timezone.utc
            )

        expenses = list(
            expenses_collection.find({
                "user_id": user_id,
                "category": category,
                "date": {
                    "$gte": month_start,
                    "$lt": next_month
                }
            })
        )

        total_spent = sum(
            float(expense.get("amount", 0))
            for expense in expenses
        )

        remaining = budget_amount - total_spent

        usage_percentage = (
            (total_spent / budget_amount) * 100
            if budget_amount > 0
            else 0
        )

        results.append({
            "budget_id": str(budget["_id"]),
            "category": category,
            "month": month.strftime("%Y-%m"),
            "budget_amount": budget_amount,
            "total_spent": round(total_spent, 2),
            "remaining": round(remaining, 2),
            "usage_percentage": round(usage_percentage, 2),
            "exceeded": total_spent > budget_amount
        })

    return {
        "message": "Budget tracking retrieved successfully",
        "budgets": results
    }