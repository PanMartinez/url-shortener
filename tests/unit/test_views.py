import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shortener.models import ShortURL

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


class TestShortUrlView:
    url = reverse("shortener:create")
    test_url = "https://example.com/test-url"

    def test_create_view_returns_201_for_new_url(self, api_client: APIClient) -> None:
        payload = {"original_url": self.test_url}
        response = api_client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["original_url"] == self.test_url
        assert ShortURL.objects.filter(code=response.data["code"]).exists()

    def test_create_view_returns_200_for_duplicate_url(self, api_client: APIClient) -> None:
        payload = {"original_url": self.test_url}
        first = api_client.post(self.url, payload, format="json")
        second = api_client.post(self.url, payload, format="json")

        assert first.status_code == status.HTTP_201_CREATED
        assert second.status_code == status.HTTP_200_OK
        assert second.data["code"] == first.data["code"]
        assert ShortURL.objects.filter(original_url=self.test_url).count() == 1

    def test_create_view_generates_code_matching_configured_length(self, api_client: APIClient) -> None:
        payload = {"original_url": self.test_url}
        response = api_client.post(self.url, payload, format="json")

        assert len(response.data["code"]) == settings.DEFAULT_CODE_LENGTH

    def test_create_view_rejects_invalid_url(self, api_client: APIClient) -> None:
        payload = {"original_url": "not-a-url"}
        response = api_client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "original_url" in response.data

    def test_create_view_rejects_missing_original_url(self, api_client: APIClient) -> None:
        response = api_client.post(self.url, {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "original_url" in response.data

    def test_expand_view_returns_short_url_data(self, api_client: APIClient) -> None:
        existing_url = ShortURL.objects.create(original_url=self.test_url, code="ABC1234")
        response = api_client.get(reverse("shortener:expand", kwargs={"code": existing_url.code}))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == existing_url.code
        assert response.data["original_url"] == existing_url.original_url

    def test_expand_view_returns_404_for_unknown_code(self, api_client: APIClient) -> None:
        response = api_client.get(reverse("shortener:expand", kwargs={"code": "MISSING"}))

        assert response.status_code == status.HTTP_404_NOT_FOUND
