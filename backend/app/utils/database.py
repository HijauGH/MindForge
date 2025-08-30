from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
import os

engine = create_async_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        if os.getenv("MODE") == "dev":
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

def get_async_session():
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

async def close():
    await engine.dispose()

def run(): asyncio.run(init_db())