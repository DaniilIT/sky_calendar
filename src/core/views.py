from rest_framework import generics

from core import serializers
from core.models import User


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer
