from typing import Any

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from shortener.models import ShortURL
from shortener.serializers import ShortURLSerializer


class ShortURLCreateView(generics.CreateAPIView[ShortURL]):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        original_url: str = serializer.validated_data["original_url"]
        already_existed = ShortURL.objects.filter(original_url=original_url).exists()
        instance = serializer.save()
        response_status = status.HTTP_200_OK if already_existed else status.HTTP_201_CREATED
        return Response(self.get_serializer(instance).data, status=response_status)


class ShortURLExpandView(generics.RetrieveAPIView[ShortURL]):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"
