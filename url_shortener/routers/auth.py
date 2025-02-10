import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from url_shortener.handlers import ErrorMessages
from url_shortener.config.dependencies import get_db
from url_shortener.domain.auth.services import (
    create_user,
    decode_token,
    get_user_by_email,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_user,
)
from url_shortener.domain.auth.models import User
from url_shortener.domain.auth.schemas import (
    UserAuthSchema,
    TokenSchema,
    UserSchema,
    RefreshTokenSchema,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    include_in_schema=True,
)


@auth_router.post("/register")
def user_register(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    if get_user_by_email(email=user_data.email, db=db):
        return {"error": "User with this email already exists"}

    user = create_user(user_data=user_data, db=db)
    return user

@auth_router.post("/access_token")
def get_access_token(
    user_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenSchema:
    user = get_user_by_email(email=user_data.username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.AUTH_USER_NOT_FOUND,
        )
    if not verify_password(
        plain_password=user_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.AUTH_INVALID_PASSWORD,
        )
    access_token = create_access_token(
        data={"sub": user.email},
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email},
    )
    return TokenSchema(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@auth_router.post("/refresh_token")
def get_refresh_token(token_data: RefreshTokenSchema):
    try:
        decoded_token = decode_token(token_data.refresh_token)
        email = decoded_token["sub"]
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.AUTH_INVALID_TOKEN,
            )

        access_token = create_access_token(data={"sub": email})
        return {"access_token": access_token}

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.AUTH_INVALID_TOKEN,
        )


@auth_router.get("/me", response_model=UserSchema)
def me(current_user: User = Depends(get_current_user)):
    return UserSchema.model_validate(current_user)
