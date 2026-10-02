from pydantic import BaseModel, Field
from datetime import datetime


class IncomeCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    description: str = ""
    date: datetime