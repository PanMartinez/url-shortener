from uuid import UUID

from url_shortener.domain.common.schemas import OrmBaseModel


class UserAuthSchema(OrmBaseModel):
    email: str
    password: str


class UserSchema(OrmBaseModel):
    id: UUID
    email: str
    is_active: bool

