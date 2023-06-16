from django.contrib import auth
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core import serializers
from core.models import User


class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user=serializer.save()
#         auth.login(request=request, user=user)
#         return Response(ProfileSerializer(user).data)

    def perform_create(self, serializer):
        user = serializer.save()
        auth.login(request=self.request, user=user)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user  # вместо queryset

    def perform_destroy(self, instance: User):
        auth.logout(self.request)


class PasswordUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        auth.update_session_auth_hash(self.request, user)
