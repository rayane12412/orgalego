"""Session SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.db.models import Base

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Crée les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dépendance FastAPI fournissant une session DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
