import pytest

from shortener.models import ShortURL
from shortener.serializers import ShortURLSerializer

pytestmark = pytest.mark.django_db


class TestShortURLSerializer:
    test_url = "https://example.com/test-url"

    def test_serializer_accepts_valid_url(self) -> None:
        serializer = ShortURLSerializer(data={"original_url": self.test_url})

        assert serializer.is_valid()

    def test_serializer_rejects_invalid_url(self) -> None:
        serializer = ShortURLSerializer(data={"original_url": "not-a-url"})

        assert not serializer.is_valid()
        assert "original_url" in serializer.errors

    def test_serializer_rejects_missing_original_url(self) -> None:
        serializer = ShortURLSerializer(data={})

        assert not serializer.is_valid()
        assert "original_url" in serializer.errors

    def test_serializer_ignores_client_supplied_code(self) -> None:
        serializer = ShortURLSerializer(data={"original_url": self.test_url, "code": "HACKED1"})
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        assert instance.code != "HACKED1"

    def test_serializer_create_returns_new_object_for_new_url(self) -> None:
        serializer = ShortURLSerializer(data={"original_url": self.test_url})
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        assert ShortURL.objects.filter(pk=instance.pk).exists()

    def test_serializer_create_is_idempotent_for_duplicate_url(self) -> None:
        first_serializer = ShortURLSerializer(data={"original_url": self.test_url})
        first_serializer.is_valid(raise_exception=True)
        first_instance = first_serializer.save()

        second_serializer = ShortURLSerializer(data={"original_url": self.test_url})
        second_serializer.is_valid(raise_exception=True)
        second_instance = second_serializer.save()

        assert second_instance.pk == first_instance.pk
        assert ShortURL.objects.filter(original_url=self.test_url).count() == 1
