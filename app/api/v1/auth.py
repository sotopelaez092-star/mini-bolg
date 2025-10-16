from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.hashing import hash_password, verify_password

router = APIRouter()
'''
@router.post("/register", response_model=UserOut)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
'''
import uuid

new_id = uuid.uuid4()#生成唯一id
@router.post("/register")
async def register_user(user_in: UserCreate, db=Depends(get_db)):
    result = await db.fetchrow("SELECT * FROM users WHERE email=$1", user_in.email)
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")

    await db.execute(
        "INSERT INTO users (id, email, hashed_password, full_name) VALUES ($1, $2, $3, $4)",
        str(new_id),
        user_in.email,
        hash_password(user_in.password),
        user_in.full_name
    )
    return {"email": user_in.email, "full_name": user_in.full_name}
