from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from server.util.config import getConfig
import threading


class DatabaseConnection:
    """Singleton database connection manager."""

    _instance: Optional["DatabaseConnection"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        config = getConfig()
        database_url = config.get_database_url()

        # Create engine with connection pooling
        self.engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,  # Set to True for SQL logging in development
        )

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self._initialized = True

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    def close_connection(self):
        """Close database connection."""
        if hasattr(self, "engine"):
            self.engine.dispose()


db_connection = DatabaseConnection()


def get_db_session() -> Session:
    """Get database session - convenience function."""
    return db_connection.get_session()
