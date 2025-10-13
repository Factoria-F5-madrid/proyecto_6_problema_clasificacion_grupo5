import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context

# allow importing backend package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import your Base
from db.database import Base  # backend/db/database.py

config = context.config
fileConfig(config.config_file_name)

# Use DATABASE_URL env var if present
db_url = os.getenv("ALEMBIC_DATABASE_URL") or os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
if db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
config.set_main_option("sqlalchemy.url", db_url)


target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
