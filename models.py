from pydantic import BaseModel,EmailStr

class ChatRequest(BaseModel):
    input:str
    session_id:str


class RegisterRequest(BaseModel):
    name:str
    email:EmailStr
    password:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"
