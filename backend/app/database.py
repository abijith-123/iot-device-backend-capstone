import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings


class Base(DeclarativeBase):
    pass


def _normalize_database_url(url: str) -> str:
    """Use psycopg 3 when a provider supplies a generic Postgres URL."""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def _runtime_database_url(url: str) -> str:
    """Keep the no-database Vercel fallback inside its writable temp directory."""
    if os.getenv("VERCEL") and url == "sqlite:///./telemetry.db":
        return "sqlite:////tmp/telemetry.db"
    return url


def _engine_options(url: str) -> dict:
    return {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {}


database_url = _normalize_database_url(_runtime_database_url(get_settings().database_url))
engine = create_engine(database_url, pool_pre_ping=True, **_engine_options(database_url))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
