from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schema import UserLoginSchema, UserRegisterSchema
from app.database.core import get_session
from app.dependencies import password_context
from app.auth import signJWT
from app.database.model import User


router = APIRouter(prefix="", tags=["Auth"])

@router.post("/registration", status_code=201)
async def registration(data: UserRegisterSchema, session: AsyncSession = Depends(get_session)):
    user = User(**data.dict())
    session.add(user)
    try:
        await session.commit()
        return {"message": "Success"}
    except IntegrityError:
        return JSONResponse(status_code=400, content={"message": "login is busy"}) 

@router.post("/login")
async def login(data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User).where(User.login==data.login))
    user: User = user.scalar() 
    if user and password_context.verify(data.password, user.password):
        return signJWT(user.id)
    return JSONResponse(status_code=400, content={"message": "Not login"}) 