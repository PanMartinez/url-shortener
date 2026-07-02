import pytest
from django.db import IntegrityError

from shortener.models import ShortURL

pytestmark = pytest.mark.django_db


class TestShortURLModel:
    test_url = "https://example.com/test-url"

    def test_str_returns_code(self) -> None:
        instance = ShortURL.objects.create(original_url=self.test_url, code="ABC1234")

        assert str(instance) == "ABC1234"

    def test_original_url_must_be_unique(self) -> None:
        ShortURL.objects.create(original_url=self.test_url, code="AAA1111")

        with pytest.raises(IntegrityError):
            ShortURL.objects.create(original_url=self.test_url, code="BBB2222")

    def test_code_must_be_unique(self) -> None:
        ShortURL.objects.create(original_url="https://example.com/one", code="SAME123")

        with pytest.raises(IntegrityError):
            ShortURL.objects.create(original_url="https://example.com/two", code="SAME123")
