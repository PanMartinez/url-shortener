import pytest
import psycopg2
from contextlib import contextmanager
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from main import get_application
from url_shortener.domain.auth.services import create_access_token
from url_shortener.config.dependencies import get_db
from url_shortener.config.settings import get_settings
from url_shortener.domain.auth.models import User
from url_shortener.domain.common.models import Base
from url_shortener.domain.urls.models import Url


ADMIN_DATABASE_URL: str = get_settings().database_url
TEST_DATABASE_NAME: str = f"{get_settings().db_name}_test_db"
TEST_DATABASE_URL: str = (
    f"{get_settings().database_url.rsplit('/', 1)[0]}/{TEST_DATABASE_NAME}"
)


@contextmanager
def _admin_db_cursor():
    connection = psycopg2.connect(ADMIN_DATABASE_URL, sslmode="disable")
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        connection.close()


def create_test_database():
    with _admin_db_cursor() as cursor:
        try:
            cursor.execute(f"CREATE DATABASE {TEST_DATABASE_NAME};")
        except psycopg2.errors.DuplicateDatabase:
            pass


def drop_test_database():
    with _admin_db_cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME};")


@pytest.fixture(scope="session")
def test_engine():
    create_test_database()
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    drop_test_database()


@pytest.fixture(scope="function")
def test_db(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def override_get_db(test_db):
    def _override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    return _override_get_db


@pytest.fixture(scope="function")
def client(override_get_db):
    app = get_application()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def auth_client(test_user, client):
    token = create_access_token(data={"sub": test_user.email})

    class AuthClient:
        def __init__(self, test_client, test_token):
            self.client = test_client
            self.token = test_token

        def request(self, method, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
            return self.client.request(method, url, headers=headers, **kwargs)

    return AuthClient(test_client=client, test_token=token)


@pytest.fixture()
def dummy_user(test_db: Session):
    def create_dummy_user(email: str, *args, **kwargs):
        existing_user: User | None = test_db.query(User).filter_by(email=email).first()
        if existing_user:
            return existing_user

        user: User = User(email=email, *args, **kwargs)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user

    return create_dummy_user


@pytest.fixture()
def test_user(dummy_user) -> User:
    user: User = dummy_user(
        email="test@user.co",
        hashed_password="",
    )
    return user


@pytest.fixture()
def dummy_url(test_db: Session):
    def create_dummy_url(*args, **kwargs):
        original_url = kwargs.pop("original_url")
        existing_url = test_db.query(Url).filter_by(original_url=original_url).first()
        if existing_url:
            return existing_url
        url = Url(original_url=original_url, *args, **kwargs)
        test_db.add(url)
        test_db.commit()
        test_db.refresh(url)
        return url

    return create_dummy_url


@pytest.fixture()
def test_url(dummy_url, test_user: User) -> Url:
    url: Url = dummy_url(
        original_url="https://www.google.com",
        shortened_url="https://go.url",
        user=test_user,
        user_ip="127.0.0.1",
        user_agent="Test User Agent",
    )
    return url
