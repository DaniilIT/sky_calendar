from rest_framework import generics, permissions

from goals import serializers


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCreateSerializer
