import os
import uuid
import urllib
from django.core import files
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django_extensions.db.fields import AutoSlugField
import requests
from bs4 import BeautifulSoup
from users.models import User


def download_file_from_url(url, file_name):
    # Stream the image from the url
    try:
        request = requests.get(url, stream=True)
    except requests.exceptions.RequestException as error:
        raise Exception(error)

    if request.status_code != requests.codes.ok:
        return None

    # Create a temporary file
    temp_file = NamedTemporaryFile(delete=True)

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        temp_file.write(block)

    temp_file.flush()
    return files.File(temp_file, name=file_name)


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

    def get_metadata(self, *args, **kwargs):
        if self.created_at is not None:
            return

        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            url_parts = urllib.parse.urlparse(self.url)
            base_url = f'{url_parts.scheme}://{url_parts.netloc}'
            if url_parts.port:
                base_url = f'{base_url}:{url_parts.port}'

            if self.icon.name is None:
                icon = soup.find("link", rel="shortcut icon")
                if icon:
                    icon_url = urllib.parse.urljoin(self.url, icon.get('href'))
                    icon_path = urllib.parse.urlparse(icon_url).path
                    icon_ext = os.path.splitext(icon_path)[1]
                    self.icon = download_file_from_url(
                        icon_url,
                        f"{str(self.id)}{icon_ext}"
                    )

            if self.image.name is None:
                image = soup.find("meta", property="og:image")
                if image:
                    image_url = urllib.parse.urljoin(
                        self.url,
                        image.get('content')
                    )
                    image_path = urllib.parse.urlparse(image_url).path
                    image_ext = os.path.splitext(image_path)[1]
                    self.image = download_file_from_url(
                        image_url,
                        f"{str(self.id)}{image_ext}"
                    )

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
