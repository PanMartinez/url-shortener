from typing import Any

from rest_framework import serializers

from shortener.codegen import generate_code
from shortener.models import ShortURL


class ShortURLCreateSerializer(serializers.Serializer[ShortURL]):
    original_url = serializers.URLField(max_length=2048)

    def create(self, validated_data: dict[str, Any]) -> ShortURL:
        original_url: str = validated_data["original_url"]
        existing = ShortURL.objects.filter(original_url=original_url).first()
        if existing is not None:
            return existing
        return ShortURL.objects.create(original_url=original_url, code=generate_code())


class ShortURLSerializer(serializers.ModelSerializer[ShortURL]):
    class Meta:
        model = ShortURL
        fields = ["code", "original_url", "created_at"]
        read_only_fields = fields
