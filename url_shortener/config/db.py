from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from url_shortener.config.settings import get_settings

engine = create_engine(get_settings().database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
