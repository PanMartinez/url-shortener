from typing import Any

from rest_framework import serializers

from shortener.codegen import generate_code
from shortener.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer[ShortURL]):
    original_url = serializers.URLField(max_length=2048)

    class Meta:
        model = ShortURL
        fields = ["code", "original_url", "created_at"]
        read_only_fields = ["code", "created_at"]

    def create(self, validated_data: dict[str, Any]) -> ShortURL:
        obj, _ = ShortURL.objects.get_or_create(
            original_url=validated_data["original_url"],
            defaults={"code": generate_code()},
        )
        return obj
