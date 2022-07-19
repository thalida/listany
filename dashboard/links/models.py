
from email.mime import image
from turtle import title
import uuid
from django.db import models
from django_extensions.db.fields import AutoSlugField
from users.models import User
from .metadata import Metadata


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    collections = models.ManyToManyField(
        'Collection',
        related_name='links',
        blank=True,
        default=None
    )
    created_by = models.ForeignKey(
        User,
        related_name='links',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['url', 'created_by'],
                name='unique_url_per_user'
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_metadata()

    def save_metadata(self):
        url_metadata = Metadata(
            self.url,
            get_filename=lambda: f"{self.id}-{self.created_by.id}"
        )
        url_metadata.fetch()
        LinkMeta.objects.update_or_create(
            link=self,
            **url_metadata.metadata,
            **url_metadata.fetch_stats,
        )


class LinkMeta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.OneToOneField(
        Link,
        related_name='link_meta',
        on_delete=models.CASCADE,
    )
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

    class Meta:
        pass


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True, null=True, default=None)
    created_by = models.ForeignKey(
        User,
        related_name='link_collections',
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
