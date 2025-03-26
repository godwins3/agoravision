from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.app.schemas.models.user import User
from sqlalchemy.orm import Session
from src.app.core.database import get_db
from src.app.core.config import settings 
from datetime import datetime, timedelta
from src.app.schemas.User import UserCreate
from passlib.context import CryptContext
import jwt as jwt_test
# Secret key and algorithm for JWT
SECRET_KEY = settings.SECRET_KEY  
ALGORITHM = settings.ALGORITHM  

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify password hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate password hash
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#  Retrieve user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#  Retrieve user by ID (for JWT verification)
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

#  Create a new user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#  Authenticate user (email & password check)
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

#  Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#  Get current user from JWT token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(settings.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        print('check point 2')
        raise credentials_exception

    # Fetch user from database
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise credentials_exception

    return user