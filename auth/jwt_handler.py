from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from config import JWT_ALGORITHM,SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime,now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})
    token=jwt.encode(to_encode,
    SECRET_KEY,
    algorithm=JWT_ALGORITHM)
    return token

def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,
        SECRET_KEY,
        algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
