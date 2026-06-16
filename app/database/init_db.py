from app.database.connection import engine

from app.database.models import Base


def create_tables():
    """Creates all tables."""
    Base.metadata.create_all(
        bind=engine
    )