from django.db import models
import uuid


class Link(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url = models.URLField(max_length=2000)
    title = models.CharField(max_length=2000)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.title} ({self.url})'
