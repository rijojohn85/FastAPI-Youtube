from sqlmodel import create_engine, text
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from src.config import Config
from sqlalchemy.orm import sessionmaker
from src.books.models import Book

engine = AsyncEngine(create_engine(url=Config.DEV_DATABASE_URL, echo=False))


async def init_db():
    async with engine.begin() as conn:

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with Session() as session:
        yield session
