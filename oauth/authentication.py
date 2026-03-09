from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from .models import OAuthToken


class OAuthSessionAuthentication(BaseAuthentication):
    """
    Authenticates:
    - Authorization: Bearer <access_token>  (custom OAuthToken table)
    - OR fallback to Django session user (request._request.user) -> OAuthToken row
    """

    def authenticate(self, request):
        # Always use the underlying Django HttpRequest to avoid DRF recursion
        raw_request = getattr(request, "_request", request)

        # 1) Bearer token from header (read from Django HttpRequest)
        auth_value = raw_request.META.get("HTTP_AUTHORIZATION", "") or ""
        auth_value = auth_value.strip()

        if auth_value:
            parts = auth_value.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                access_token = parts[1].strip()
                token = (
                    OAuthToken.objects.select_related("user")
                    .filter(access_token=access_token, expires_at__gt=now())
                    .order_by("-expires_at")
                    .first()
                )
                if not token:
                    raise AuthenticationFailed("Invalid or expired access token")

                if not token.user or not token.user.is_active:
                    raise AuthenticationFailed("User inactive or missing")

                return (token.user, token)

        # 2) Session fallback (read from Django HttpRequest, NOT request.user)
        django_user = getattr(raw_request, "user", None)
        if not django_user or not django_user.is_authenticated:
            return None

        token = (
            OAuthToken.objects.filter(user=django_user, expires_at__gt=now())
            .order_by("-expires_at")
            .first()
        )
        if not token:
            return None

        return (django_user, token)
