from django.contrib import admin
from .models import Identity

@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ("nickname", "website_or_game", "email", "created_on")
    search_fields = ("nickname", "email", "website_or_game")