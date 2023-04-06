from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from authentication.models import User


class Collection(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='collections'
    )

    title = models.CharField(max_length=2000)
    subtitle = models.CharField(max_length=2000, blank=True)
    description = models.TextField(blank=True)
    links = models.ManyToManyField(
        'core.Link',
        related_name='collections',
        blank=True,
        through='core.CollectionLink'
    )
    tags = models.ManyToManyField(
        'core.UserTag',
        related_name='collections',
        blank=True,
    )
    is_public = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'


@receiver(post_save, sender=User)
def create_user_collection(sender, instance, created, **kwargs):
    if not created:
        return

    Collection.objects.create(
        created_by=instance,
        title=f'My Collection'
    )
