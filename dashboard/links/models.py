import uuid
from django.db import models
from django_extensions.db.fields import AutoSlugField


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(unique=True)
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None
    )
    description = models.TextField(
        blank=True,
        null=True,
        default=None
    )
    image = models.URLField(
        blank=True,
        null=True,
        default=None
    )
    collections = models.ManyToManyField(
        'Collection',
        related_name='links',
        null=True,
        blank=True,
        default=None
    )
    created_by = models.ForeignKey(
        'auth.User',
        related_name='links',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        ordering = ('-created_at',)


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        unique=True,
        populate_from=['name']
    )
    description = models.TextField(blank=True, null=True, default=None)
    created_by = models.ForeignKey(
        'auth.User',
        related_name='link_collections',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
