from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.serializers import ProfileSerializer
from goals.models import Goal, GoalCategory, GoalComment

# Category


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    # автоматическое заполнение текущего пользователя
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        # на вход только title
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


# Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed deleted category')
        if value.user != self.context['request'].user:
            raise PermissionDenied
        return value


class GoalSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    # user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed category')
        if value.user != self.context['request'].user:
            raise PermissionDenied
        return value


# Comment


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    # goal = serializers.PrimaryKeyRelatedField(
    #     queryset=Goal.objects.exclude(status=Goal.Status.archived)
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_comment(self, value: GoalComment):
        if value.user != self.context['request'].user:
            raise PermissionDenied
        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')

    def validate_comment(self, value: GoalCategory):
        if value.user != self.context['request'].user:
            raise PermissionDenied
        return value
