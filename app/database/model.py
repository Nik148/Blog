from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Table, UniqueConstraint,
                        update, case, select, PrimaryKeyConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from .core import Base


class Likes(Base):
    __tablename__ = "likes"

    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    __table_args__ = (
        PrimaryKeyConstraint(post_id, user_id),
    )
    post = relationship(
        'Post', back_populates='likes_models', lazy="select"
    )

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(), index=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)

    posts = relationship(
        "Post", back_populates="author", lazy="select", cascade="all,delete"
    )

    def __init__(self, login, password):
        self.login = login
        self.password = password


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    date = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    likes = Column(Integer, default=0)

    author = relationship(
        "User", back_populates="posts", lazy="select"
    )

    likes_models = relationship(
        "Likes", cascade="all,delete", back_populates="post", lazy="select"
    )

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text

    @hybrid_method
    def is_like(self, user_id):
        return case(
            (Post.id.in_(
                select(Likes.post_id).where(Likes.user_id == user_id)
            ), True),
            else_=False
        )

    @staticmethod
    async def minusLike(id, value, session):
        await session.execute(
            update(Post).where(Post.id == id).values(likes=Post.likes - value)
        )

    @staticmethod
    async def plusLike(id, value, session):
        await session.execute(
            update(Post).where(Post.id == id).values(likes=Post.likes + value)
        )
