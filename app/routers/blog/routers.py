from fastapi import APIRouter, Depends, Request, Response, Cookie
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, case
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from typing import List
from app.auth import JWTBearer
from app.database.core import get_session
from app.database.model import Post, likes, User
from app.dependencies import templates
from .schema import BlogSchema


router = APIRouter(prefix="", tags=["Blog"])

@router.get("/blog", response_model=List[BlogSchema])
async def blog(
            request: Request,
            token = Depends(JWTBearer(check_cookie=True)), 
            session: AsyncSession = Depends(get_session),
):
    case_stmt = case(
                    (Post.id.in_(
                        select(likes.c.post_id).where(likes.c.user_id==token["user_id"])
                    ), True),
                    else_=False
                )
    result = await session.execute(select(Post, case_stmt)
                                  .join(Post.author)
                                  .options(contains_eager(Post.author))
                                  .order_by(Post.date.desc()))
    result = result.all()
    posts = []
    for post in result:
        post[0].isLiked = post[1]
        posts.append(post[0])
    return templates.TemplateResponse("blog.html", {"request": request, 
                                                    "posts":posts,
                                                    "user_id": token["user_id"],
                                                    "access_token": request.cookies["access_token"]},
                                                    )

@router.get("/blog/login", response_model=List[BlogSchema])
async def blog_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/blog/register", response_model=List[BlogSchema])
async def blog_register(request: Request):

    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/blog/add_post", response_model=List[BlogSchema])
async def add_post(request: Request,
                   token = Depends(JWTBearer(check_cookie=True))):

    return templates.TemplateResponse("add_post.html", {"request": request,
                                                        "access_token": request.cookies["access_token"]})
