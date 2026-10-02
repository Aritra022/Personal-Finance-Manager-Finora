
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is missing from .env")

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

database = client["personal_finance"]

# Collections
users_collection = database["users"]
expenses_collection = database["expenses"]
income_collection = database["income"]
budgets_collection = database["budgets"]
goals_collection = database["goals"]
recurring_collection = database["recurring_transactions"]
notifications_collection = database["notifications"]