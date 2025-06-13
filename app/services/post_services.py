from sqlmodel import sql
from app.schema import Post
from app.database import get_session


async def read_posts(skip: int = 0, limit: int = 10):
    async with get_session() as session:
        statement = sql.select(Post).offset(skip).limit(limit)
        result = await session.exec(statement)
        posts = result.all()
        return posts

async def post_creator(post_data: dict):
    """Create a new post in the database"""
    print(f"Creating post with data: {post_data}")
    
    try:
        async with get_session() as session:
            # Create a Post model instance instead of using dict
            new_post = Post(
                title=post_data["title"],
                content=post_data.get("content", ""),
                media_url=post_data.get("media_url"),
                author_id=post_data["author_id"]
            )
            
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
            return {
                "id": new_post.id,
                "title": new_post.title,
                "content": new_post.content,
                "media_url": new_post.media_url,
                "author_id": new_post.author_id,
                "created_at": new_post.created_at,
                "updated_at": new_post.updated_at
            }
            
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Database error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        await session.rollback()
        logging.error(f"Unexpected error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def update_post(post_id: int, post_data: Post):
    async with get_session() as session:
        statement = sql.select(Post).where(Post.id == post_id)
        result = await session.exec(statement)
        post = result.one_or_none()
        
        if post is None:
            return None
        
        for key, value in post_data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        
        await session.commit()
        await session.refresh(post)
        return post

async def delete_post(post_id: int):
    async with get_session() as session:
        statement = sql.select(Post).where(Post.id == post_id)
        result = await session.exec(statement)
        post = result.one_or_none()
        
        if post is None:
            return None
        
        await session.delete(post)
        await session.commit()
        return post

async def get_post_by_id(post_id: int):
    async with get_session() as session:
        statement = sql.select(Post).where(Post.id == post_id)
        result = await session.exec(statement)
        post = result.one_or_none()
        return post

async def get_posts_by_author(author_id: int, skip: int = 0, limit: int = 10):
    async with get_session() as session:
        statement = sql.select(Post).where(Post.author_id == author_id).offset(skip).limit(limit)
        result = await session.exec(statement)
        posts = result.all()
        return posts

