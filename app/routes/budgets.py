from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.mongodb import budgets_collection
from app.schemas.budget import BudgetCreate
from app.security.jwt import verify_access_token


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        user_id = verify_access_token(
            credentials.credentials
        )

        return ObjectId(user_id)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# ==========================================
# CREATE BUDGET
# ==========================================

@router.post("/")
def create_budget(
    budget: BudgetCreate,
    user_id: ObjectId = Depends(get_current_user_id)
):
    budget_month = budget.month.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    # Check whether this category already
    # has a budget for the selected month
    existing_budget = budgets_collection.find_one({
        "user_id": user_id,
        "category": budget.category,
        "month": budget_month
    })

    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail="A budget for this category already exists for this month."
        )

    budget_data = {
        "user_id": user_id,
        "category": budget.category,
        "monthly_limit": budget.monthly_limit,
        "month": budget_month,
        "created_at": datetime.now(timezone.utc)
    }

    result = budgets_collection.insert_one(
        budget_data
    )

    return {
        "message": "Budget created successfully",
        "budget_id": str(result.inserted_id)
    }


# ==========================================
# GET ALL BUDGETS
# ==========================================

@router.get("/")
def get_budgets(
    user_id: ObjectId = Depends(get_current_user_id)
):
    budgets = list(
        budgets_collection.find({
            "user_id": user_id
        }).sort("month", -1)
    )

    result = []

    for budget in budgets:

        result.append({
            "id": str(budget["_id"]),
            "category": budget["category"],
            "monthly_limit": budget["monthly_limit"],
            "month": budget["month"].isoformat()
        })

    return result


# ==========================================
# UPDATE BUDGET
# ==========================================

@router.put("/{budget_id}")
def update_budget(
    budget_id: str,
    budget: BudgetCreate,
    user_id: ObjectId = Depends(get_current_user_id)
):
    try:
        budget_object_id = ObjectId(budget_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid budget ID"
        )

    budget_month = budget.month.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    existing_budget = budgets_collection.find_one({
        "_id": budget_object_id,
        "user_id": user_id
    })

    if not existing_budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    duplicate_budget = budgets_collection.find_one({
        "_id": {"$ne": budget_object_id},
        "user_id": user_id,
        "category": budget.category,
        "month": budget_month
    })

    if duplicate_budget:
        raise HTTPException(
            status_code=400,
            detail="A budget for this category already exists for this month."
        )

    budgets_collection.update_one(
        {
            "_id": budget_object_id,
            "user_id": user_id
        },
        {
            "$set": {
                "category": budget.category,
                "monthly_limit": budget.monthly_limit,
                "month": budget_month
            }
        }
    )

    return {
        "message": "Budget updated successfully"
    }


# ==========================================
# DELETE BUDGET
# ==========================================

@router.delete("/{budget_id}")
def delete_budget(
    budget_id: str,
    user_id: ObjectId = Depends(get_current_user_id)
):
    try:
        budget_object_id = ObjectId(budget_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid budget ID"
        )

    result = budgets_collection.delete_one({
        "_id": budget_object_id,
        "user_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    return {
        "message": "Budget deleted successfully"
    }