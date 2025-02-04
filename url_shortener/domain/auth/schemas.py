from uuid import UUID

from url_shortener.domain.common.schemas import OrmBaseModel


class UserAuthSchema(OrmBaseModel):
    email: str
    password: str


class UserSchema(OrmBaseModel):
    id: UUID
    email: str
    is_active: bool


class TokenSchema(OrmBaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AccessTokenSchema(OrmBaseModel):
    email: str


class RefreshTokenSchema(OrmBaseModel):
    refresh_token: str