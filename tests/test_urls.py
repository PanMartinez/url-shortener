import pytest
from httpx import Client
from url_shortener.domain.auth.models import User
from url_shortener.domain.urls.models import Url


class TestCreateShortenedUrlRouter:
    create_shorten_url_endpoint = "/api/urls/shorten_url"

    def test_get_shortened_url_endpoint(self, test_user: User, auth_client: Client):
        payload = {"original_url": "https://google.com"}
        response = auth_client.request(
            method="POST",
            url=self.create_shorten_url_endpoint,
            json=payload
        )
        assert response.status_code == 200
        assert response.json()["original_url"] == payload["original_url"]
        shortened_url = response.json()["shortened_url"]
        assert shortened_url

        another_response = auth_client.request(
            method="POST",
            url=self.create_shorten_url_endpoint,
            json=payload
        )
        assert another_response.status_code == 200
        assert another_response.json()["original_url"] == payload["original_url"]
        assert another_response.json()["shortened_url"] == shortened_url


    @pytest.mark.parametrize(
        'invalid_url,response_code',
        [
            (44, 422),
            (True, 422),
            ("randomstring", 422),
            ("invalidprotocol://google.com", 422),
        ],
    )
    def test_get_shortened_url_endpoint_with_invalid_url(self, invalid_url: str, response_code: int, auth_client: Client):
        payload = {"original_url": invalid_url}
        response = auth_client.request(
            method="POST",
            url=self.create_shorten_url_endpoint,
            json=payload
        )
        assert response.status_code == response_code

    @pytest.mark.parametrize(
        'authenticated,response_code',
        [
            (True, 200),
            (False, 401),
        ],
    )
    def test_create_url_by_short_authentication(
            self,
            authenticated: bool,
            response_code: int,
            auth_client: Client,
            client: Client,
            test_user: User,
            test_url: Url
    ):
        if authenticated:
            client = auth_client

        payload = {"original_url": "https://google.com"}
        response = client.request(
            method="POST",
            url=self.create_shorten_url_endpoint,
            json=payload
        )
        assert response.status_code == response_code


class TestGetUrlRouter:
    get_url_endpoint = "/api/urls/get_url"

    @pytest.mark.parametrize(
        'shorten_url,response_code',
        [
            ("https://go.url", 200),
            ("randomstring", 400),
            ("https://google.com", 400),
        ],
    )
    def test_get_url_by_short_endpoint_val(
            self,
            shorten_url: str,
            response_code: int,
            test_user: User,
            auth_client: Client,
            test_url: Url
    ):
        pyload = {
            "shortened_url": shorten_url
        }
        response = auth_client.request(
            method="POST",
            url=self.get_url_endpoint,
            json=pyload
        )
        assert response.status_code == response_code


    @pytest.mark.parametrize(
        'authenticated,response_code',
        [
            (True, 200),
            (False, 200),
        ],
    )
    def test_get_url_by_short_authentication(
            self,
            authenticated: bool,
            response_code: int,
            auth_client: Client,
            client: Client,
            test_user: User,
            test_url: Url
    ):
        if authenticated:
            client = auth_client

        pyload = {
            "shortened_url": test_url.shortened_url
        }
        response = client.request(
            method="POST",
            url=self.get_url_endpoint,
            json=pyload
        )
        assert response.status_code == response_code