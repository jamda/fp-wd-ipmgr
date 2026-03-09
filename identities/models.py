import uuid
from django.db import models
from django.conf import settings


class Identity(models.Model):
    # A unique ID for GDPR-friendly referencing (non-sequential, non-guessable)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="identities")
    # Context / domain of use
    CONTEXT_CHOICES = [
        ("professional", "Professional"),
        ("academic", "Academic"),
        ("gaming", "Gaming"),
        ("social", "Social"),
        ("personal", "Personal"),
        ("other", "Other"),
    ]

    context_domain = models.CharField(
        max_length=32,
        choices=CONTEXT_CHOICES,
        default="personal",
        help_text="Context in which this identity is intended to be used"
    )
    # Core fields
    website_or_game = models.CharField(max_length=255)  # e.g. "Twitch", "Steam", "Gmail"
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    nickname = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True)

    is_visible_in_api = models.BooleanField(default=True)

    # Auto timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Identity"
        verbose_name_plural = "Identities"
        ordering = ["-created_on"]  # newest first

    def __str__(self):
        return f"{self.nickname or self.email or 'Identity'} ({self.website_or_game})"