from pydantic import BaseModel, Field
from datetime import datetime

class RecurringTransactionCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    transaction_type: str
    category: str
    frequency: str
    start_date: datetime
    description: str = ""