from fastapi import APIRouter, Depends, Request, Response, Cookie
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, case
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from typing import List
from app.auth import JWTBearer
from app.database.core import get_session
from app.database.model import Post
from app.dependencies import templates
from .schema import BlogSchema


router = APIRouter(prefix="", tags=["Blog"])


@router.get("/")
async def main(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse("/blog")
    return RedirectResponse("/blog/login")


@router.get("/blog", response_model=List[BlogSchema])
async def blog(
    request: Request,
    token=Depends(JWTBearer(check_cookie=True)),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Post, Post.is_like(token["user_id"]))
                                   .join(Post.author)
                                   .options(contains_eager(Post.author))
                                   .order_by(Post.date.desc()))
    result = result.all()
    posts = []
    for post in result:
        post[0].isLiked = post[1]
        posts.append(post[0])

    return templates.TemplateResponse("blog.html", {"request": request,
                                                    "posts": posts,
                                                    "user_id": token["user_id"],
                                                    "access_token": request.cookies["access_token"]},
                                      )


@router.get("/blog/login", response_model=List[BlogSchema])
async def blog_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/blog/register", response_model=List[BlogSchema])
async def blog_register(request: Request):

    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/blog/logout")
async def blog_logout(request: Request, response: Response):
    response.delete_cookie(key="access_token")
    return RedirectResponse("/blog/login")


@router.get("/blog/add_post", response_model=List[BlogSchema])
async def add_post(request: Request,
                   token=Depends(JWTBearer(check_cookie=True))):

    return templates.TemplateResponse("add_post.html", {"request": request,
                                                        "access_token": request.cookies["access_token"]})
