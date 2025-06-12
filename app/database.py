from sqlmodel import create_engine, Session, SQLModel
from app.schema import User, Post  

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session(): 
    """Get a new SQLModel session."""
    return Session(engine)