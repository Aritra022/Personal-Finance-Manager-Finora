
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)
# Register page
@router.get("/register", response_class=HTMLResponse)
@router.get("/register/", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

# Login page
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )
    


# Dashboard page
@router.get("/dashboard", response_class=HTMLResponse)
@router.get("/dashboard/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


# Expenses webpage
@router.get("/expenses-page", response_class=HTMLResponse)
@router.get("/expenses-page/", response_class=HTMLResponse)
def expenses_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="expenses.html",
        context={}
    )
# Income webpage
@router.get("/income-page", response_class=HTMLResponse)
@router.get("/income-page/", response_class=HTMLResponse)
def income_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="income.html",
        context={}
    )

# Budgets webpage
@router.get("/budgets-page", response_class=HTMLResponse)
@router.get("/budgets-page/", response_class=HTMLResponse)
def budgets_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="budgets.html",
        context={}
    )

# Goals webpage
@router.get("/goals-page", response_class=HTMLResponse)
@router.get("/goals-page/", response_class=HTMLResponse)
def goals_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="goals.html",
        context={}
    )

# Analytics webpage
@router.get("/analytics-page", response_class=HTMLResponse)
@router.get("/analytics-page/", response_class=HTMLResponse)
def analytics_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={}
    )

# Recurring Transactions webpage
@router.get("/recurring-page", response_class=HTMLResponse)
@router.get("/recurring-page/", response_class=HTMLResponse)
def recurring_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="recurring.html",
        context={}
    )

# Notifications webpage
@router.get("/notifications-page", response_class=HTMLResponse)
@router.get("/notifications-page/", response_class=HTMLResponse)
def notifications_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="notifications.html",
        context={}
    )
#AI BOT
@router.get("/ai-page/", response_class=HTMLResponse)
@router.get("/ai-page", response_class=HTMLResponse)
def ai_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ai.html",
        context={}
    )

    # Profile Settings webpage
@router.get("/profile-page/", response_class=HTMLResponse)
@router.get("/profile-page", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={}
    )