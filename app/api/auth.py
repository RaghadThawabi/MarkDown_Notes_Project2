from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.core.security import hash_password
from app.services.authorization_service import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(email: str, password: str,fullname:str, db: AsyncSession = Depends(get_db)):
    user = User(email=email, hashed_password=hash_password(password),full_name=fullname)
    db.add(user)
    await db.commit()
    return {"msg": "user created"}

@router.post("/login")
async def login(id: str):
    token = create_access_token({"token": id})
    return {"access_token": token}
