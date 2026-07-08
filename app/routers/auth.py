from fastapi import Depends, APIRouter

from app.database import connect_db
from app.schemas import (
    UserSchema,
    UserRegisterSchema,
    UserLoginSchema,
    TokenSchema
)

from typing import Annotated

from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

DBSession = Annotated[Session, Depends(connect_db)]

@router.post("/register", response_model=UserSchema, status_code=201)
def rigster_user(db: DBSession, user: UserRegisterSchema):
    user_repository = UserRepository(db)

    join_user = user_repository.register(user)
    return join_user

@router.post("/signin", response_model=TokenSchema)
def login(db: DBSession, user: UserLoginSchema):
    user_repository = UserRepository(db)

    acccess_token = user_repository.signin(user)
    return { "access_token": acccess_token }
