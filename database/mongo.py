from pymongo import MongoClient
from config import MONGODB_URI

mongo_client=MongoClient(MONGODB_URI)
db=mongo_client["ai_pdf"]
print("MongoDB Connected Successfully!")