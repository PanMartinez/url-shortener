from url_shortener.domain.auth.models import User


def test_healthcheck(test_user: User):
    assert test_user
