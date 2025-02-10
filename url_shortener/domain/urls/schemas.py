from uuid import UUID
from pydantic import field_validator
from url_shortener.handlers import ErrorMessages
from url_shortener.domain.common.schemas import OrmBaseModel


class UrlCreateSchema(OrmBaseModel):
    original_url: str

    @field_validator("original_url", mode="before")
    @classmethod
    def validate_url(cls, value):
        if not isinstance(value, str) or not value.startswith(("http://", "https://")):
            raise ValueError(ErrorMessages.URL_INVALID_URL)
        return value


class UrlRetrieveSchema(OrmBaseModel):
    shortened_url: str


class UrlSchema(OrmBaseModel):
    id: UUID
    shortened_url: str
    original_url: str
    user_ip: str
    user_agent: str
