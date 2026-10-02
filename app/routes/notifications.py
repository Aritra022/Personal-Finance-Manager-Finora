from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database.mongodb import (
    budgets_collection,
    expenses_collection,
    goals_collection,
    notifications_collection
)
from app.security.jwt import verify_access_token


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# ---------------------------------------------------------
# GET NOTIFICATIONS
# ---------------------------------------------------------
@router.get("/")
def get_notifications(
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    user_id = ObjectId(current_user)
    now = datetime.now(timezone.utc)

    active_source_keys = []

    # =====================================================
    # 1. CHECK BUDGETS
    # =====================================================

    budgets = budgets_collection.find({
        "user_id": user_id
    })

    for budget in budgets:

        category = budget.get("category")
        month = budget.get("month")

        # Your Budget schema uses monthly_limit
        budget_amount = float(
            budget.get("monthly_limit", 0)
        )

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
                month.year + 1,
                1,
                1,
                tzinfo=timezone.utc
            )
        else:
            next_month = datetime(
                month.year,
                month.month + 1,
                1,
                tzinfo=timezone.utc
            )

        expenses = expenses_collection.find({
            "user_id": user_id,
            "category": category,
            "date": {
                "$gte": month_start,
                "$lt": next_month
            }
        })

        total_spent = sum(
            float(expense.get("amount", 0))
            for expense in expenses
        )

        if budget_amount <= 0:
            continue

        usage = (total_spent / budget_amount) * 100

        source_key = f"budget:{budget['_id']}"
        active_source_keys.append(source_key)

        # ---------------------------------------------
        # Budget exceeded
        # ---------------------------------------------
        if total_spent > budget_amount:

            notification_data = {
                "type": "budget_exceeded",
                "title": "Budget Exceeded",
                "message": (
                    f"You exceeded your {category} budget "
                    f"by {round(total_spent - budget_amount, 2)}."
                ),
                "category": category,
                "usage_percentage": round(usage, 2),
                "source_key": source_key,
                "user_id": user_id,
                "updated_at": now,
                "active": True
            }

            notifications_collection.update_one(
                {
                    "user_id": user_id,
                    "source_key": source_key
                },
                {
                    "$set": notification_data,
                    "$setOnInsert": {
                        "is_read": False,
                        "dismissed": False,
                        "created_at": now
                    }
                },
                upsert=True
            )

        # ---------------------------------------------
        # Budget warning
        # ---------------------------------------------
        elif usage >= 80:

            notification_data = {
                "type": "budget_warning",
                "title": "Budget Almost Used",
                "message": (
                    f"You have used {round(usage, 2)}% "
                    f"of your {category} budget."
                ),
                "category": category,
                "usage_percentage": round(usage, 2),
                "source_key": source_key,
                "user_id": user_id,
                "updated_at": now,
                "active": True
            }

            notifications_collection.update_one(
                {
                    "user_id": user_id,
                    "source_key": source_key
                },
                {
                    "$set": notification_data,
                    "$setOnInsert": {
                        "is_read": False,
                        "dismissed": False,
                        "created_at": now
                    }
                },
                upsert=True
            )

        else:
            # Budget is healthy again
            notifications_collection.update_one(
                {
                    "user_id": user_id,
                    "source_key": source_key
                },
                {
                    "$set": {
                        "active": False,
                        "updated_at": now
                    }
                }
            )

    # =====================================================
    # 2. CHECK FINANCIAL GOALS
    # =====================================================

    goals = goals_collection.find({
        "user_id": user_id
    })

    for goal in goals:

        target = float(
            goal.get("target_amount", 0)
        )

        current = float(
            goal.get("current_amount", 0)
        )

        source_key = f"goal:{goal['_id']}"

        if target > 0 and current >= target:

            active_source_keys.append(source_key)

            # Your Goal schema uses name
            goal_name = goal.get(
                "name",
                "Financial Goal"
            )

            notification_data = {
                "type": "goal_achieved",
                "title": "Financial Goal Achieved!",
                "message": (
                    f"Congratulations! You achieved your "
                    f"goal: {goal_name}."
                ),
                "goal_title": goal_name,
                "source_key": source_key,
                "user_id": user_id,
                "updated_at": now,
                "active": True
            }

            notifications_collection.update_one(
                {
                    "user_id": user_id,
                    "source_key": source_key
                },
                {
                    "$set": notification_data,
                    "$setOnInsert": {
                        "is_read": False,
                        "dismissed": False,
                        "created_at": now
                    }
                },
                upsert=True
            )

        else:
            notifications_collection.update_one(
                {
                    "user_id": user_id,
                    "source_key": source_key
                },
                {
                    "$set": {
                        "active": False,
                        "updated_at": now
                    }
                }
            )

    # =====================================================
    # 3. GET ACTIVE NOTIFICATIONS
    # =====================================================

    notifications = list(
        notifications_collection.find({
            "user_id": user_id,
            "active": True,
            "dismissed": {
                "$ne": True
            }
        }).sort(
            "created_at",
            -1
        )
    )

    result = []

    for notification in notifications:

        result.append({
            "id": str(notification["_id"]),
            "type": notification.get("type"),
            "title": notification.get("title"),
            "message": notification.get("message"),
            "category": notification.get("category"),
            "goal_title": notification.get("goal_title"),
            "usage_percentage": notification.get(
                "usage_percentage"
            ),
            "is_read": notification.get(
                "is_read",
                False
            ),
            "created_at": notification.get(
                "created_at"
            )
        })

    return {
        "message": "Notifications retrieved successfully",
        "total_notifications": len(result),
        "notifications": result
    }


# ---------------------------------------------------------
# MARK ONE NOTIFICATION AS READ
# ---------------------------------------------------------
@router.patch("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: str,
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid notification ID"
        )

    user_id = ObjectId(current_user)
    notification_object_id = ObjectId(notification_id)

    result = notifications_collection.update_one(
        {
            "_id": notification_object_id,
            "user_id": user_id
        },
        {
            "$set": {
                "is_read": True,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification marked as read"
    }


# ---------------------------------------------------------
# MARK ALL NOTIFICATIONS AS READ
# ---------------------------------------------------------
@router.patch("/read-all")
def mark_all_notifications_as_read(
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    user_id = ObjectId(current_user)

    result = notifications_collection.update_many(
        {
            "user_id": user_id,
            "active": True,
            "dismissed": {
                "$ne": True
            },
            "is_read": False
        },
        {
            "$set": {
                "is_read": True,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "All notifications marked as read",
        "updated_count": result.modified_count
    }


# ---------------------------------------------------------
# DELETE / DISMISS NOTIFICATION
# ---------------------------------------------------------
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: str,
    current_user: str = Depends(verify_access_token)
):
    if not ObjectId.is_valid(current_user):
        raise HTTPException(
            status_code=401,
            detail="Invalid user authentication"
        )

    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid notification ID"
        )

    user_id = ObjectId(current_user)
    notification_object_id = ObjectId(notification_id)

    result = notifications_collection.update_one(
        {
            "_id": notification_object_id,
            "user_id": user_id
        },
        {
            "$set": {
                "dismissed": True,
                "active": False,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification deleted successfully"
    }