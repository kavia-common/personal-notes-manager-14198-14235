from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """
    A personal note owned by a user.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    content = models.TextareaField = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # set on create
    updated_at = models.DateTimeField(auto_now=True)      # set on each update

    def __str__(self) -> str:
        return f"{self.title} (owner={self.owner.username})"
