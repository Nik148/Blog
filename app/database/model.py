from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table,UniqueConstraint, update
from sqlalchemy.orm import relationship
from datetime import datetime
from .core import Base

likes = Table('likes', Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('user_id', Integer, ForeignKey('user.id')),
    UniqueConstraint('post_id', 'user_id')
)

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

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text

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
