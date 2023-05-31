from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from goals import serializers
from goals.filters import GoalDateFilter
from goals.models import Goal, GoalCategory, GoalComment

# Category


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategoryCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = LimitOffsetPagination
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('title', 'created')
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.request.user.categories.filter(is_deleted=False)
        # return self.model.objects.filter(
        #     user=self.request.user, is_deleted=False
        # )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.categories.filter(is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance


# Goal


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    serializer_class = serializers.GoalCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GoalListView(generics.ListAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = GoalDateFilter
    ordering_fields = ('title', 'created')
    ordering = ('title',)
    search_fields = ('title', 'description')

    def get_queryset(self):
        return self.request.user.goals.filter(~Q(status=self.model.Status.archived))
        # return self.model.objects.filter(
        #     Q(user_id=self.request.user.id) & ~Q(status=self.model.Status.archived)
        # )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.goals.filter(~Q(status=self.model.Status.archived))

    def perform_destroy(self, instance: Goal):
        instance.status = self.model.Status.archived
        instance.save(update_fields=('status',))
        return instance


# Comment


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields = ('goal',)
    ordering = ('-created',)

    def get_queryset(self):
        return self.request.user.comments


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.comments
