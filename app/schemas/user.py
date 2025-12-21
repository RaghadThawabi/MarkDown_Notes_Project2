from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserName(BaseModel):
    full_name: str

class UserLogin(BaseModel):
    user:UserCreate

class UserSignUp(BaseModel):
    username: UserName
    user: UserCreate

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
