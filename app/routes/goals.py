from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.mongodb import goals_collection
from app.schemas.goal import GoalCreate
from app.security.jwt import verify_access_token


router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
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


# Create Goal
@router.post("/")
def create_goal(
    goal: GoalCreate,
    user_id: ObjectId = Depends(get_current_user_id)
):
    if goal.current_amount > goal.target_amount:
        raise HTTPException(
            status_code=400,
            detail="Current amount cannot be greater than target amount."
        )

    goal_data = {
        "user_id": user_id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "target_date": goal.target_date,
        "created_at": datetime.now(timezone.utc)
    }

    result = goals_collection.insert_one(goal_data)

    return {
        "message": "Goal created successfully",
        "goal_id": str(result.inserted_id)
    }


# Get Goals
@router.get("/")
def get_goals(
    user_id: ObjectId = Depends(get_current_user_id)
):
    goals = list(
        goals_collection.find({
            "user_id": user_id
        }).sort("target_date", 1)
    )

    result = []

    for goal in goals:
        result.append({
            "id": str(goal["_id"]),
            "name": goal["name"],
            "target_amount": goal["target_amount"],
            "current_amount": goal["current_amount"],
            "target_date": goal["target_date"].isoformat()
        })

    return result


# Update Goal
@router.put("/{goal_id}")
def update_goal(
    goal_id: str,
    goal: GoalCreate,
    user_id: ObjectId = Depends(get_current_user_id)
):
    try:
        goal_object_id = ObjectId(goal_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid goal ID"
        )

    if goal.current_amount > goal.target_amount:
        raise HTTPException(
            status_code=400,
            detail="Current amount cannot be greater than target amount."
        )

    existing_goal = goals_collection.find_one({
        "_id": goal_object_id,
        "user_id": user_id
    })

    if not existing_goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    goals_collection.update_one(
        {
            "_id": goal_object_id,
            "user_id": user_id
        },
        {
            "$set": {
                "name": goal.name,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "target_date": goal.target_date
            }
        }
    )

    return {
        "message": "Goal updated successfully"
    }


# Delete Goal
@router.delete("/{goal_id}")
def delete_goal(
    goal_id: str,
    user_id: ObjectId = Depends(get_current_user_id)
):
    try:
        goal_object_id = ObjectId(goal_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid goal ID"
        )

    result = goals_collection.delete_one({
        "_id": goal_object_id,
        "user_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return {
        "message": "Goal deleted successfully"
    }