from rest_framework import serializers
from .models import Identity

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = [
            "id",
            "context_domain",
            "website_or_game",
            "first_name",
            "last_name",
            "email",
            "nickname",
            "avatar_url",
            "is_visible_in_api",
            "created_on",
            "last_modified",
        ]
        read_only_fields = ["id", "user", "created_on", "last_modified"]