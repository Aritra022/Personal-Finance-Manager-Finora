from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.mongodb import client, database

from app.routes.auth import router as auth_router
from app.routes.expenses import router as expenses_router
from app.routes.income import router as income_router
from app.routes.budgets import router as budget_router
from app.routes.goals import router as goals_router
from app.routes.dashboard import router as dashboard_router
from app.routes.recurring import router as recurring_router
from app.routes.analytics import router as analytics_router

from app.routes import budget_tracking
from app.routes import notifications
from app.routes import transaction_search
from app.routes import pages

from app.routes.ai import router as ai_router

# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI()


# ==========================================
# Project Directories
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# Uploaded Files
# ==========================================

UPLOADS_DIR = BASE_DIR / "uploads"

UPLOADS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads"
)


# ==========================================
# Frontend Static Files
# ==========================================

STATIC_DIR = BASE_DIR / "app" / "static"

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ==========================================
# API Routers
# ==========================================

app.include_router(auth_router)

app.include_router(expenses_router)

app.include_router(income_router)

app.include_router(budget_router)

app.include_router(goals_router)

app.include_router(dashboard_router)

app.include_router(recurring_router)

app.include_router(analytics_router)

app.include_router(ai_router)

app.include_router(
    budget_tracking.router
)

app.include_router(
    notifications.router
)

app.include_router(
    transaction_search.router
)


# ==========================================
# Frontend Pages
# ==========================================

app.include_router(
    pages.router
)


# ==========================================
# Home / API Test
# ==========================================

@app.get("/")
def home():
    return {
        "message":
        "Personal Finance Manager API is running"
    }


# ==========================================
# MongoDB Test
# ==========================================

@app.post("/test-database")
def test_database():

    client.admin.command("ping")

    database["test"].insert_one({
        "message":
        "MongoDB connected through Swagger!"
    })

    return {
        "message":
        "MongoDB connected and test data inserted!"
    }