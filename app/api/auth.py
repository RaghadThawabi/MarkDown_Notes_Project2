from fastapi import APIRouter, status,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.schemas.user import Token, UserLogin, UserCreate
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name
    )

    db.add(new_user)
    await db.commit()

    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    result = await db.execute(select(User).where(User.email == email))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({"user_id": str(db_user.id)})

    return {"access_token": access_token, "token_type": "bearer"}