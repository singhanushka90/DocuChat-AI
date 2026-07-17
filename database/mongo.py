from pymongo import MongoClient
from config import MONGODB_URI

mongo_client=MongoClient(MONGODB_URI)
print("MongoDB Connected Successfully!")