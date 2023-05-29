from rest_framework import filters, generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from goals import serializers
from goals.models import GoalCategory


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('title', 'created')
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCategorySerializer

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=('is_deleted',))
        return instance
