from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings

# check_same_thread is false for a better behavior with fastAPI (multiple threads.
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Base class for the ORM (used by car and rental models).
class Base(DeclarativeBase):
    pass


# yield db session - generate Session object. getting nothing, returns nothing
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db

        # commit the changes to db only of the whole transaction went without exceptions
        db.commit()
    except Exception:
        # rollback when something went wrong in the middle of a transaction
        db.rollback()
        raise
    finally:
        db.close()