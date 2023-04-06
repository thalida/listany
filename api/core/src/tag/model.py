from django.db import models
from django.template.defaultfilters import slugify
import uuid


class Tag(models.Model):
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
        related_name='tags'
    )

    slug = models.SlugField(max_length=2000, editable=False)
    label = models.CharField(max_length=2000)

    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug'
            ),
        ]

    def __str__(self):
        return f'{self.label}'

    def clean(self):
        self.label = self.label.strip().lower()

        if not self.slug:
            self.slug = slugify(self.label)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)
