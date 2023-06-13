from django.contrib import auth
from rest_framework import generics, permissions

from core import serializers
from core.models import User


class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


# class LoginView(generics.GenericAPIView):
#     serializer_class = serializers.LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user=serializer.save()
#         login(request=request, user=user)
#         return Response(ProfileSerializer(user).data)


class LoginView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

    def perform_create(self, serializer):
        auth.login(request=self.request, user=serializer.save())


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user  # вместо queryset

    def perform_destroy(self, instance: User):
        auth.logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.UpdatePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
