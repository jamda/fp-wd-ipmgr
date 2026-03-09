from django.urls import path
from .views import oauth_callback_view, oauth_test_view

urlpatterns = [
    path("callback/", oauth_callback_view, name="oauth_callback"),
    path("get-token/", oauth_test_view, name="oauth_test"),
]