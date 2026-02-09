import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name='posts', null=True, blank=True
    )
    company_name = models.CharField(max_length=255)
    logo_placeholder = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()
    detailed_description = models.TextField()
    images = ArrayField(models.URLField(), blank=True, default=list)
    videos = ArrayField(models.URLField(), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
