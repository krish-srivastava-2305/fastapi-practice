import sqlmodel as sql
from app.schema import User
from app.database import get_session

async def check_if_exists(user_email: str):
    """Checks if user with given email exists"""
    async with get_session() as session:
        result = await session.execute(sql.select(User).where(User.email == user_email))
        return result.scalars().first()

async def create_user(user: User):
    """Creates new user in the database"""
    db_user = User(**user.dict())

    async with get_session() as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

    return db_user
