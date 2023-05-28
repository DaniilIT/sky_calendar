from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response

from core import serializers

# from core.models import User


class UserCreateView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class LoginView(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())  # с использованием cookies
        return Response(serializer.data, status=status.HTTP_201_CREATED)
