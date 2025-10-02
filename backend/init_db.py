# archivo para inicializar la base de datos
import asyncio
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import engine, Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    asyncio.run(init_db())