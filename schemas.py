from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    date: str


class ExpenseResponse(BaseModel):
    id: str
    title: str
    amount: float
    category: str
    date: str