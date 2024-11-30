from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


postgres = "postgres"  # e.g., "postgres"
samrudh = "samrudh"  # e.g., "samrudh"
localhost = "localhost"  # Your database host, usually "localhost"
database_name = "Fastapi_CRUD"  # Your database name



engine = create_async_engine(
    f"postgresql+asyncpg://{postgres}:{samrudh}@{localhost}:5432/{database_name}",
    future=True,
)

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
