import os
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv

load_dotenv()

# aqui leemos el BASE_URL del archivo .env

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()