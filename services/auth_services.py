from sqlalchemy.orm import Session
from models.user import User
from jose import jwt
from datetime import datetime, timedelta
import hashlib

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(db: Session, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    hashed_password = hash_password(password)
    db_user = User(email=email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user credentials"""
    user = get_user_by_email(db, email)
    if not user or user.password != hash_password(password):
        return None
    return user

def create_access_token(data: dict) -> str:
    """Create JWT token with 24h expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_token(db: Session, token: str) -> User:
    """Get user from JWT token"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub")
    return db.query(User).filter(User.id == user_id).first()