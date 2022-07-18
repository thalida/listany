import uuid
from django.db import models
from django_extensions.db.fields import AutoSlugField
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
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
    icon = models.URLField(blank=True, null=True, default=None)
    image = models.URLField(blank=True, null=True, default=None)
    link_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None
    )
    collections = models.ManyToManyField(
        'Collection',
        related_name='links',
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
        constraints = [
            models.UniqueConstraint(
                fields=['url', 'created_by'],
                name='unique_url_per_user'
            )
        ]

    def get_metadata(self, *args, **kwargs):
        if self.created_at is not None:
            return

        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            url_parts = urlparse(self.url)
            base_url = f'{url_parts.scheme}://{url_parts.netloc}'
            if url_parts.port:
                base_url = f'{base_url}:{url_parts.port}'

            if self.icon is None:
                icon = soup.find("link", rel="shortcut icon")
                print(icon.get('href'))
                self.icon = f"{base_url}{icon.get('href')}" if icon else None

            if self.title is None:
                og_title = soup.find("meta", property="og:title")
                if og_title:
                    self.title = og_title.get('content')
                else:
                    self.title = soup.title.string

            if self.description is None or len(self.description) == 0:
                og_desc = soup.find("meta", property="og:description")
                if og_desc:
                    self.description = og_desc.get('content')
                else:
                    meta_desc = soup.find("meta", property="description")
                    self.description = meta_desc.get('content')

            if self.image is None:
                image = soup.find("meta", property="og:image")
                self.image = image.get('content') if image else None

            if self.link_type is None:
                og_type = soup.find("meta", property="og:type")
                self.link_type = og_type.get('content') if og_type else None

        except Exception as error:
            raise error

    def save(self, *args, **kwargs):
        self.get_metadata()
        self.full_clean()
        super().save(*args, **kwargs)


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
