from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.schemas import UserCreate, UserLogin, Token
from models.database import get_db
from services.auth_service import create_user, authenticate_user, create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user and return access token"""
    db_user = create_user(db, user.email, user.password)
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"token": token}

@router.post("/login", response_model=Token)
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(data={"sub": str(authenticated_user.id)})
    return {"token": token}