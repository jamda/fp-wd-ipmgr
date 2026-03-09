from django import forms
from .models import Identity

class IdentityForm(forms.ModelForm):
    class Meta:
        model = Identity
        fields = [
            "context_domain",
            "website_or_game",
            "first_name",
            "last_name",
            "email",
            "nickname",
            "avatar_url",
        ]