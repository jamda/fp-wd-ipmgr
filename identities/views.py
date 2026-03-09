from rest_framework.viewsets import ModelViewSet
from oauth2_provider.contrib.rest_framework import ( OAuth2Authentication,TokenHasScope,)
from rest_framework.permissions import IsAuthenticated
from oauth.authentication import OAuthSessionAuthentication
from .models import Identity
from .serializers import IdentitySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Identity
from .forms import IdentityForm

@login_required
def welcome(request):
    identities = Identity.objects.filter(user=request.user).order_by("-created_on")

    if request.method == "POST":
        form = IdentityForm(request.POST)
        if form.is_valid():
            identity = form.save(commit=False)
            identity.user = request.user
            identity.save()
            return redirect("identities:welcome")
    else:
        form = IdentityForm()

    return render(request, "identities/welcome.html", {
        "form": form,
        "identities": identities,
    })


@login_required
def identity_edit(request, pk):
    identity = get_object_or_404(Identity, pk=pk, user=request.user)

    if request.method == "POST":
        form = IdentityForm(request.POST, instance=identity)
        if form.is_valid():
            form.save()
            return redirect("identities:welcome")
    else:
        form = IdentityForm(instance=identity)

    return render(request, "identities/identity_edit.html", {
        "form": form,
        "identity": identity,
    })

@login_required
def identity_delete(request, pk):
    identity = get_object_or_404(Identity, pk=pk, user=request.user)

    if request.method == "POST":
        identity.delete()
        return redirect("identities:welcome")

    return render(request, "identities/identity_delete.html", {
        "identity": identity,
    })
@login_required
def toggle_api_visibility(request, identity_id):
    identity = get_object_or_404(Identity, id=identity_id, user=request.user)
    identity.is_visible_in_api = not identity.is_visible_in_api
    identity.save(update_fields=["is_visible_in_api"])
    return redirect("identities:welcome")

class IdentityViewSet(ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]

    required_scopes = ["identity"]

@login_required
def identity_add(request):
    if request.method == "POST":
        form = IdentityForm(request.POST)
        if form.is_valid():
            identity = form.save(commit=False)
            identity.user = request.user
            identity.save()
            return redirect("identities:welcome")
    else:
        form = IdentityForm()

    return render(request, "identities/identity_add.html", {"form": form})