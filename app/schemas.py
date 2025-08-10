from pydantic import BaseModel, EmailStr


# Request schema for signup/login
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response schema for successful login/signup
class Token(BaseModel):
    access_token: str
    token_type: str
