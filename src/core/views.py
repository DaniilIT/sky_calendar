from django.contrib import auth
from rest_framework import generics, permissions

from core import serializers
from core.models import User


class UserCreateView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


# class LoginView(generics.GenericAPIView):
#     # queryset = User.objects.all()
#     serializer_class = serializers.LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         login(request=request, user=serializer.save())  # с использованием cookies
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.LoginSerializer

    def perform_create(self, serializer):
        auth.login(request=self.request, user=serializer.save())


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance: User):
        auth.logout(self.request)
