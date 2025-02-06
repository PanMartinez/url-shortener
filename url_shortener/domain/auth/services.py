from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status

from url_shortener.handlers import ErrorMessages
from url_shortener.config.settings import get_settings
from url_shortener.config.dependencies import get_db, oauth2_scheme
from url_shortener.domain.auth.enums import JwtTokenType
from url_shortener.domain.auth.models import User
from url_shortener.domain.auth.schemas import UserAuthSchema, AccessTokenSchema

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user_data: UserAuthSchema, db: Session) -> User:
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_jwt_token(data: dict, token_type: JwtTokenType) -> str:
    to_encode = data.copy()
    if token_type == JwtTokenType.ACCESS:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=get_settings().access_token_expire_minutes
        )
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=get_settings().refresh_token_expire_days
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, get_settings().jwt_secret_key, algorithm=get_settings().algorithm
    )
    return encoded_jwt


def create_access_token(data: dict):
    return create_jwt_token(data=data, token_type=JwtTokenType.ACCESS)


def create_refresh_token(data: dict):
    return create_jwt_token(data=data, token_type=JwtTokenType.REFRESH)


def decode_token(token):
    return jwt.decode(
        token, get_settings().jwt_secret_key, algorithms=[get_settings().algorithm]
    )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.AUTH_INVALID_CREDENTIALS,
            )
        AccessTokenSchema(email=email)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.AUTH_INVALID_TOKEN,
        )
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.AUTH_USER_NOT_FOUND,
        )
    return user
