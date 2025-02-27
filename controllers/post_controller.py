from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.schemas import PostCreate, PostResponse
from models.database import get_db
from services.post_service import create_post, get_user_posts, delete_post
from dependencies.auth import get_current_user
from models.user import User

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def add_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post for authenticated user"""
    db_post = create_post(db, post.text, current_user.id)
    return db_post

@router.get("/", response_model=list[PostResponse])
async def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all posts for authenticated user"""
    return get_user_posts(db, current_user.id)

@router.delete("/{post_id}")
async def delete_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific post for authenticated user"""
    success = delete_post(db, post_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not authorized"
        )
    return {"message": "Post deleted successfully"}