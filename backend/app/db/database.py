from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# 1. Build the connection string from your settings
DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


# 2. The engine — the connection to Postgres (created once)
engine = create_engine(DATABASE_URL)

# 3. The session factory — makes sessions for running queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The base — your models will inherit from this
Base = declarative_base()