import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from url_shortener.config.settings import get_settings
from url_shortener.handlers import ErrorMessages
from url_shortener.config.dependencies import get_db
from url_shortener.domain.auth.models import User
from url_shortener.domain.auth.services import get_current_user
from url_shortener.domain.urls.services import (
    create_url,
    update_url,
    get_url_by_short,
    get_url_by_original,
)
from url_shortener.domain.urls.schemas import (
    UrlSchema,
    UrlCreateSchema,
    UrlRetrieveSchema,
)

urls_router = APIRouter(
    prefix="/urls",
    tags=["urls"],
    include_in_schema=True,
)

logger = logging.getLogger(__name__)


@urls_router.post("/shorten_url", response_model=UrlSchema)
def shorten_url(
    request: Request,
    url_data: UrlCreateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UrlSchema:
    client_ip = request.client.host if request.client else "Unknown"
    user_agent = request.headers.get("User-Agent", "Unknown")
    if existing_url := get_url_by_original(original_url=url_data.original_url, db=db):
        if not len(existing_url.shortened_url) == get_settings().shortened_url_length:
            logger.warning(
                f"URL {existing_url.original_url} was setup before on different length, overriding"
            )
            existing_url = update_url(
                url_data=url_data, current_user=current_user, db=db
            )
        return UrlSchema.model_validate(existing_url)

    return UrlSchema.model_validate(
        create_url(
            url_data=url_data,
            current_user=current_user,
            user_ip=client_ip,
            user_agent=user_agent,
            db=db,
        )
    )


@urls_router.post("/get_url", response_model=UrlSchema)
def get_url(url_data: UrlRetrieveSchema, db: Session = Depends(get_db)) -> UrlSchema:
    if url := get_url_by_short(shortened_url=url_data.shortened_url, db=db):
        return UrlSchema.model_validate(url)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorMessages.URL_NOT_FOUND,
    )
