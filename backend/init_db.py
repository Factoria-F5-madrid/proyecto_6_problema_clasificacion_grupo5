import asyncio
import os
from backend.db.database import engine, Base

async def init_db():
    """
    Crea tablas de base de datos declaradas en SQLAlchemy Base. Seguro para desarrolladores. En producción, usar Alembic. 
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DB inicializada correctamente.")

if __name__ == "__main__":
    asyncio.run(init_db())