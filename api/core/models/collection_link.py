from django.db import models


class CollectionLink(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE
    )
    link = models.ForeignKey(
        "core.Link",
        on_delete=models.CASCADE
    )
    collection = models.ForeignKey(
        "core.Collection",
        on_delete=models.CASCADE,
    )

    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.link} - {self.collection}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['collection', 'link'],
                name='unique_collection_link'
            ),
        ]
