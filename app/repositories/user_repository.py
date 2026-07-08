from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User
from app.schemas import UserRegisterSchema, UserLoginSchema

from app.security import (
    create_access_token,
    hashed_password,
    verify_password
)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, user: UserRegisterSchema):
        existed_user = self.db.query(User).filter(User.email == user.email).first()

        if existed_user is not None:
            raise HTTPException(status_code=400)
        
        join_user = User(
            username = user.username,
            email = user.email,
            password = hashed_password(user.password)
        )

        self.db.add(join_user)
        self.db.commit()
        self.db.refresh(join_user)

        return join_user
    
    def signin(self, user: UserLoginSchema):
        existed = self.db.query(User).filter(User.email == user.email).first()

        if existed is None:
            raise HTTPException(
                status_code=401,
                detail="Not Found user info.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not verify_password(user.password, existed.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        acccess_token = create_access_token(data={"sub": existed.email})

        return acccess_token