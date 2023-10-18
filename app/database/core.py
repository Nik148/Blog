from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from config import Config



Base = declarative_base()
engine = create_async_engine(Config.DB_URL)
async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session