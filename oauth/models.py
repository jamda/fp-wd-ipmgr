from django.conf import settings
from django.db import models

class OAuthToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OAuth token for {self.user}"