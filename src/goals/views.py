from django.db.models import Q
from rest_framework import filters, generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from goals import serializers
from goals.models import Goal, GoalCategory


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCategoryCreateSerializer


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
        # self.request.user.categories.filter(is_deleted=False)
        return self.model.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCategorySerializer

    def get_queryset(self):
        # self.request.user.categories.filter(is_deleted=False)
        return self.model.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=('is_deleted',))
        return instance


class GoalCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('title', 'created')
    ordering = ('title',)
    search_fields = ('title', 'description')

    def get_queryset(self):
        # self.request.user.goals.filter(~Q(status=self.model.Status.archived))
        return self.model.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=self.model.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GoalSerializer

    def get_queryset(self):
        # self.request.user.goals.filter(~Q(status=self.model.Status.archived))
        return self.model.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=self.model.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.status = self.model.Status.archived
        instance.save(update_fields=('status',))
        return instance
