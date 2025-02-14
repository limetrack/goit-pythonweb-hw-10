from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from conf.config import app_config


try:
    async_engine = create_async_engine(
        app_config.DATABASE_URL,
        echo=True,
    )
    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    Base = declarative_base()
except OperationalError as e:
    print(f"Error connecting to the database: {e}")
