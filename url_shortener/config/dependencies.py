from fastapi.security import OAuth2PasswordBearer
from url_shortener.config.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/access_token")
