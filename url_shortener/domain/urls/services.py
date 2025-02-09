import string
import random
from sqlalchemy.orm import Session

from url_shortener.config.settings import get_settings
from url_shortener.domain.auth.models import User
from url_shortener.domain.urls.models import Url
from url_shortener.domain.urls.schemas import UrlCreateSchema


def create_url(url_data: UrlCreateSchema, current_user: User, db: Session) -> Url:
    new_url = Url(
        original_url=url_data.original_url,
        shortened_url=get_shortened_url(),
        user=current_user,
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def update_url(url_data: UrlCreateSchema, current_user: User, db: Session) -> Url:
    url = get_url_by_original(original_url=url_data.original_url, db=db)
    url.original_url = url_data.original_url
    url.shortened_url = get_shortened_url()
    url.user = current_user
    db.commit()
    db.refresh(url)
    return url


def get_shortened_url() -> str:
    return ''.join(random.choices((string.ascii_letters + string.digits), k=get_settings().shortened_url_length))


def get_url_by_short(shortened_url: str, db: Session) -> Url | None:
    return db.query(Url).filter(Url.shortened_url == shortened_url).first()


def get_url_by_original(original_url: str, db: Session) -> Url | None:
    return db.query(Url).filter(Url.original_url == original_url).first()

