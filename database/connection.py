from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from config.settings import settings, logger

# Create engine
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True  # checks connection health before executing commands
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise e

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Context manager to ensure database sessions are closed correctly."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
