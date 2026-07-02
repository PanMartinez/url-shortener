from django.db import models


class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048, unique=True)
    code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code
