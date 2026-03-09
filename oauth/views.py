import requests
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now

from .models import OAuthToken


@login_required
def oauth_test_view(request):
    """
    Starts the authorization code flow by redirecting to DOT authorize endpoint.
    """
    client_id = settings.OAUTH_CLIENT_ID
    redirect_uri = "http://localhost:8000/oauth/callback/"
    scope = "identity"

    authorize_url = (
        f"/o/authorize/?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
    )
    return redirect(authorize_url)


@login_required
def oauth_callback_view(request):
    """
    Receives ?code=... then exchanges it for an access token at /o/token/,
    then stores it in oauth.OAuthToken for the logged-in user.
    """
    code = request.GET.get("code")
    if not code:
        return HttpResponseBadRequest("Missing code")

    token_url = "http://localhost:8000/o/token/"
    redirect_uri = "http://localhost:8000/oauth/callback/"

    r = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
        },
        timeout=10,
    )

    if r.status_code != 200:
        return HttpResponseBadRequest(f"Token exchange failed: {r.status_code} {r.text}")

    token_json = r.json()
    access_token = token_json["access_token"]
    expires_in = int(token_json.get("expires_in", 3600))

    OAuthToken.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": access_token,
            "expires_at": now() + timedelta(seconds=expires_in),
        },
    )

    #return HttpResponse("OK: token stored. Now call /api/identities/ (session or Bearer).")
    return HttpResponse(access_token)