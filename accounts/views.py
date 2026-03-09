from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("identities:welcome")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # IMPORTANT for OAuth: honor ?next=... (e.g. /o/authorize/...)
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            # Default: single welcome page (identities)
            return redirect("identities:welcome")

        # invalid login: render template with error
        return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    # GET request: show login form (and keep next in the template)
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("identities:welcome")

@login_required
def welcome_view(request):
    return render(request, "accounts/welcome.html")