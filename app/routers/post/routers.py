from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from sqlalchemy.exc import IntegrityError
from app.auth import JWTBearer
from app.database.core import get_session
from app.database.model import Post, likes
from .schema import PostGetSchema, PostCreateSchema, LikeSchema


router = APIRouter(prefix="", tags=["Post"])

@router.post("/post")
async def create_post(
            data: PostCreateSchema,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)):
    post = Post(user_id=token["user_id"], **data.dict())
    session.add(post)
    await session.commit()
    return JSONResponse(status_code=201, content={"message":"Post created"})

@router.get("/post/{post_id}", response_model=PostGetSchema)
async def get_post(
            post_id: int,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)
            ):
    post = await session.execute(select(Post).where(Post.id==post_id))
    post: Post = post.scalar()
    if not post:
        return JSONResponse(status_code=404, content={"message":"Post not find"})
    return post

@router.put("/post/{post_id}", response_model=PostGetSchema)
async def update_post(
            data: PostCreateSchema,
            post_id: int,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)
            ):
    post = await session.execute(update(Post)
                                 .where(Post.id==post_id)
                                 .where(Post.user_id==token["user_id"])
                                 .values(data.dict()))
    if post.rowcount == 0:
        return JSONResponse(status_code=404, content={"message":"Do not change this post"})
    await session.commit()
    return JSONResponse(status_code=201, content={"message":"Post updated"})

@router.delete("/post/{post_id}")
async def delete_post(
            post_id: int,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)
            ):
    post = await session.execute(select(Post).where(and_(Post.id==post_id,
                                                         Post.user_id==token["user_id"])))
    post: Post = post.scalar()
    if not post:
        return JSONResponse(status_code=404, content={"message":"Post not find"})
    await session.delete(post)
    await session.commit()
    # if not post:
    #     return JSONResponse(status_code=404, content={"message":"Post not find"})
    return JSONResponse(status_code=200, content={"message":"Post deleted"})

@router.post('/like_increment')
async def like_increment(
            data: LikeSchema,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)       
            ):
    try:
        await session.execute(likes.insert().values(post_id=data.post_id, user_id=token["user_id"]))
    except IntegrityError:
        return JSONResponse(status_code=400, content={"message":"Like already set or not find"})
    await Post.plusLike(data.post_id, 1, session)
    await session.commit()
    return JSONResponse(status_code=200, content={"message":"Like created"})

@router.delete('/like_decrement')
async def like_increment(
            data: LikeSchema,
            token = Depends(JWTBearer()), 
            session: AsyncSession = Depends(get_session)       
            ):
    like = await session.execute(likes.delete().where(and_(likes.c.post_id==data.post_id,
                                                    likes.c.user_id==token["user_id"])))
    if like.rowcount == 0:
        return JSONResponse(status_code=404, content={"message":"Like not find"})
    await Post.minusLike(data.post_id, 1, session)
    await session.commit()
    return JSONResponse(status_code=200, content={"message":"Like deleted"})
