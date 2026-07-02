from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import connect_db
from app.models import User

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer()

settings = get_settings()

def hashed_password(password: str):
    return password_hash.hash(password)

def verify_password(input_password: str, hashed_password: str):
    return password_hash.verify(input_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE)
    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')

    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(connect_db)):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception
    
    return user