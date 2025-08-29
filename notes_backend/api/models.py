from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """
    A personal note owned by a user.

    Fields:
    - owner: FK to auth.User, owner of the note
    - title: short title of the note
    - content: free-form text content (optional)
    - created_at: timestamp when created
    - updated_at: timestamp when last updated
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    # Store the note body; optional so blank is allowed.
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # set on create
    updated_at = models.DateTimeField(auto_now=True)      # set on each update

    def __str__(self) -> str:
        """Human-readable representation used in admin and logs."""
        return f"{self.title} (owner={self.owner.username})"
