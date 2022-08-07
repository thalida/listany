# Listany - Copyright (C) 2022  Thalida Noel

import uuid
from django.db import models
from django_extensions.db.fields import AutoSlugField
from users.models import User
from .metadata import Metadata


class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.ForeignKey(
        'Link',
        related_name='bookmarks',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    collections = models.ManyToManyField(
        'Collection',
        related_name='bookmarks',
        blank=True,
        default=None
    )
    created_by = models.ForeignKey(
        User,
        related_name='bookmarks',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by.username}'s {self.link.url}"

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['link', 'created_by'],
                name='unique_link_per_user'
            )
        ]


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
    icon = models.ImageField(
        upload_to='links/icons/',
        blank=True,
        null=True,
        default=None
    )
    image = models.ImageField(
        upload_to='links/images/',
        blank=True,
        null=True,
        default=None
    )
    image_alt = models.TextField(
        blank=True,
        null=True,
        default=None
    )
    link_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None
    )
    theme_color = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None
    )
    curated_by = models.ForeignKey(
        User,
        related_name='links',
        on_delete=models.CASCADE,
    )

    is_auto_fetch_enabled = models.BooleanField(default=True)
    is_fetch_allowed = models.BooleanField(
        blank=True,
        null=True,
        default=None
    )
    is_fetch_icon_allowed = models.BooleanField(
        blank=True,
        null=True,
        default=None
    )
    is_fetch_image_allowed = models.BooleanField(
        blank=True,
        null=True,
        default=None
    )
    last_fetched_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if self.created_at is None and self.is_auto_fetch_enabled:
            url_metadata = Metadata(
                self.url,
                get_filename=lambda: f"{self.id}"
            )
            url_metadata.fetch()
            self.title = url_metadata.metadata["title"]
            self.description = url_metadata.metadata["description"]
            self.icon = url_metadata.metadata["icon"]
            self.image = url_metadata.metadata["image"]
            self.image_alt = url_metadata.metadata["image_alt"]
            self.link_type = url_metadata.metadata["link_type"]
            self.is_fetch_allowed = url_metadata.fetch_stats["is_fetch_allowed"]
            self.is_fetch_icon_allowed = url_metadata.fetch_stats["is_fetch_icon_allowed"]
            self.is_fetch_image_allowed = url_metadata.fetch_stats["is_fetch_image_allowed"]
            self.last_fetched_at = url_metadata.fetch_stats["last_fetched_at"]
            self.theme_color = url_metadata.metadata["theme_color"]

        super().save(*args, **kwargs)


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True, null=True, default=None)
    created_by = models.ForeignKey(
        User,
        related_name='collections',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'created_by'],
                name='unique_collection_per_user'
            )
        ]
