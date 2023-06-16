from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals import permissions, serializers
from goals.filters import GoalDateFilter
from goals.models import Board, Goal, GoalCategory, GoalComment

# Board


class BoardCreateView(generics.CreateAPIView):
    model = Board
    permissions = (IsAuthenticated,)
    serializer_class = serializers.BoardCreateSerializer

    # def perform_create(self, serializer):
    #     BoardParticipant.objects.create(user=self.request.user, board=serializer.save(),
    #                                     role=BoardParticipant.Role.owner)


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = (IsAuthenticated, permissions.BoardPermissions)
    serializer_class = serializers.BoardListSerializer

    pagination_class = LimitOffsetPagination
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self) -> list[Board]:
        return self.model.objects.prefetch_related('participants').filter(
            participants__user=self.request.user,
            is_deleted=False
        )


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = (IsAuthenticated, permissions.BoardPermissions)
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


# Category


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategoryCreateSerializer
    permission_classes = (IsAuthenticated, permissions.GoalCategoryPermissions)


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = (IsAuthenticated, permissions.GoalCategoryPermissions)

    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ('board',)
    ordering_fields = ('title', 'created')
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self):
        # return self.request.user.categories.filter(is_deleted=False)
        return self.model.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = (IsAuthenticated, permissions.GoalCategoryPermissions)  # IOORO

    def get_queryset(self):
        # return self.request.user.categories.filter(is_deleted=False)
        return self.model.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            # Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
            instance.goals.update(status=Goal.Status.archived)
        return instance


# Goal


class GoalCreateView(generics.CreateAPIView):
    # model = Goal
    serializer_class = serializers.GoalCreateSerializer
    permission_classes = (IsAuthenticated, permissions.GoalPermissions)


class GoalListView(generics.ListAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = (IsAuthenticated, permissions.GoalPermissions)

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
        # return self.request.user.goals.filter(~Q(status=self.model.Status.archived))
        return self.model.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=self.model.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = (IsAuthenticated, permissions.GoalPermissions)

    def get_queryset(self):
        # return self.request.user.goals.filter(~Q(status=self.model.Status.archived))
        return self.model.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=self.model.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.status = self.model.Status.archived
        instance.save(update_fields=('status',))
        return instance


# Comment


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentCreateSerializer
    permission_classes = (IsAuthenticated, permissions.CommentsPermissions)


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = (IsAuthenticated, permissions.CommentsPermissions)

    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields = ('goal',)
    ordering = ('-created',)

    def get_queryset(self):
        # return self.request.user.comments
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = (IsAuthenticated, permissions.CommentsPermissions)  # IOORO

    def get_queryset(self):
        # return self.request.user.comments
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )
