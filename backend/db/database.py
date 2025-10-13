import os
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv

load_dotenv()

# aqui leemos el BASE_URL del archivo .env

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:root@127.0.0.1:5432/airline_satisfaction_db")

engine = create_async_engine(DATABASE_URL, echo=True , future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True

)

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Base class for models
Base = declarative_base()