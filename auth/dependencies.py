from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from bson import ObjectId

from auth.jwt_handler import verify_access_token
from database.collections import users_collection

security=HTTPBearer()
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    print("Token Received:",token)
    payload=verify_access_token(token)
    print("Payload:",payload)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired token")
    user_id=payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token payload missing user_id")
    user=users_collection.find_one({"_id":ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    user["_id"]=str(user["_id"])
    return user

