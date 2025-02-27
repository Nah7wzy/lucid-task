from sqlalchemy.orm import Session
from models.post import Post
from fastapi_cache.decorator import cache

def create_post(db: Session, text: str, user_id: int) -> Post:
    """Create a new post"""
    db_post = Post(text=text, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@cache(expire=300)  # 5 minutes cache
def get_user_posts(db: Session, user_id: int) -> list[Post]:
    """Get all posts for a user with caching"""
    return db.query(Post).filter(Post.user_id == user_id).all()

def delete_post(db: Session, post_id: int, user_id: int) -> bool:
    """Delete a post if it belongs to the user"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == user_id
    ).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False