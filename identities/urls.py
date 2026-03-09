from django.urls import path
from . import views

app_name = 'identities'

urlpatterns = [
    path("welcome/", views.welcome, name="welcome"),
    path("add/", views.identity_add, name="identity_add"),
    path("edit/<uuid:pk>/", views.identity_edit, name="identity_edit"),
    path("delete/<uuid:pk>/", views.identity_delete, name="identity_delete"),
    path("identity/<uuid:identity_id>/toggle-api/", views.toggle_api_visibility, name="toggle_api_visibility"),
]