from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestShortURLe2e:
    create_url = reverse("shortener:create")
    test_url = "https://example.com/test-url"

    def test_create_then_expand_returns_original_url(self, db: None, api_client: APIClient) -> None:
        create_response = api_client.post(self.create_url, {"original_url": self.test_url}, format="json")
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data.keys() == {"code"}
        code = create_response.data["code"]

        expand_response = api_client.get(reverse("shortener:expand", kwargs={"code": code}))

        assert expand_response.status_code == status.HTTP_200_OK
        assert expand_response.data.keys() == {"original_url"}
        assert expand_response.data["original_url"] == self.test_url

    def test_create_twice_then_expand_is_idempotent(self, db: None, api_client: APIClient) -> None:
        first_create = api_client.post(self.create_url, {"original_url": self.test_url}, format="json")
        second_create = api_client.post(self.create_url, {"original_url": self.test_url}, format="json")
        assert first_create.data["code"] == second_create.data["code"]

        expand_response = api_client.get(reverse("shortener:expand", kwargs={"code": first_create.data["code"]}))

        assert expand_response.status_code == status.HTTP_200_OK
        assert expand_response.data["original_url"] == self.test_url
