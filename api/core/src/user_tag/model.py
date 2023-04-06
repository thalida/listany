from django.db import models
import uuid


class UserTag(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        "core.Tag",
        on_delete=models.CASCADE
    )
    color = models.CharField(max_length=7, blank=True)
    description = models.TextField(blank=True)

    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tag}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tag'],
                name='unique_user_tag'
            ),
        ]
