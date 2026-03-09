from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Identity
from .serializers import IdentitySerializer

class IdentityListCreateAPI(generics.ListCreateAPIView):
    serializer_class = IdentitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # List only identities that are visible in the API
        return Identity.objects.filter(user=self.request.user, is_visible_in_api=True)

    def perform_create(self, serializer):
        # Always attach identity to the authenticated user
        serializer.save(user=self.request.user)


class IdentityDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IdentitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow retrieve/update/delete for visible identities of this user's
        return Identity.objects.filter(user=self.request.user, is_visible_in_api=True)

class IdentityByContextAPI(generics.ListAPIView):
    serializer_class = IdentitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        context_domain = self.kwargs["context_domain"]
        return Identity.objects.filter(user=self.request.user, is_visible_in_api=True, context_domain__iexact=context_domain)


class IdentityByNicknameAPI(generics.ListAPIView):
    serializer_class = IdentitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nickname = self.kwargs["nickname"]
        return Identity.objects.filter(user=self.request.user, is_visible_in_api=True, nickname__iexact=nickname)


class IdentityByEmailAPI(generics.ListAPIView):
    serializer_class = IdentitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.kwargs["email"]
        return Identity.objects.filter(user=self.request.user, is_visible_in_api=True, email__iexact=email)