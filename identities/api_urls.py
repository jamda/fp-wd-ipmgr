from django.urls import path
from .api_views import IdentityListCreateAPI, IdentityDetailAPI, IdentityByContextAPI, IdentityByNicknameAPI, IdentityByEmailAPI

urlpatterns = [
    path("identities/", IdentityListCreateAPI.as_view(), name="identity-list-create"),
    path("identities/<uuid:pk>/", IdentityDetailAPI.as_view(), name="identity-detail"),
    path("identities/context/<str:context_domain>/", IdentityByContextAPI.as_view(), name="identity-by-context"),
    path("identities/nickname/<str:nickname>/", IdentityByNicknameAPI.as_view(), name="identity-by-nickname"),
    path("identities/email/<str:email>/", IdentityByEmailAPI.as_view(), name="identity-by-email"),
]