import sqlmodel as sql
from app.schema import User
from app.database import get_session

def check_if_exists(user_email):
    """Checks if user with given email exists"""
    with get_session() as session:
        user = session.query(User).filter(User.email == user_email).first()
        return user
