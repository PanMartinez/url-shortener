from url_shortener.domain.auth.models import User


def test_register_endpoint(client, test_db):
    payload = {
        "email": "test@user.com",
        "password": "password"
    }
    response = client.request(method="POST", url="api/auth/register", json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]
    new_user = test_db.query(User).filter(User.email == payload["email"]).first()
    assert new_user


def test_me_endpoint(auth_client, test_user: User):
    response = auth_client.request(method="GET", url="api/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
