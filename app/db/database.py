from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the engine to talk to our SQLite database
# check_same_thread=False is needed for SQLite with FastAPI
engine = create_engine(
    settings.DB_URL, connect_args={"check_same_thread": False}
)

# This is our session factory (how we get a connection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class for our models
Base = declarative_base()

# Utility function to get a database session for our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
