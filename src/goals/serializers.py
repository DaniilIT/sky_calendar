from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import (
    Board, BoardParticipant, Goal, GoalCategory, GoalComment,
)

# Board


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'is_deleted', 'created', 'updated')

    def create(self, validated_data: dict) -> Board:
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantsSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices[1:])
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantsSerializer(many=True)

    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data):
        # owner = validated_data.pop('user')

        with transaction.atomic():
            if validated_data.get('participants'):
                new_participants = validated_data.pop('participants')
                new_by_id = {part['user'].id: part for part in new_participants}
                old_participants = instance.participants.exclude(user=self.context['request'].user)  # owner

                for old_participant in old_participants:
                    if old_participant.user_id not in new_by_id:
                        old_participant.delete()
                    else:
                        if old_participant.role != new_by_id[old_participant.user_id]['role']:
                            old_participant.role = new_by_id[old_participant.user_id]['role']
                            old_participant.save()
                        new_by_id.pop(old_participant.user_id)

                for new_part in new_by_id.values():
                    BoardParticipant.objects.create(
                        board=instance, user=new_part['user'], role=new_part['role']
                    )

            if title := validated_data['title']:
                instance.title = title

            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')


# Category


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    # автоматическое заполнение текущего пользователя
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        # на вход только title
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')

    def validate_board(self, value: Board):
        if value.is_deleted:
            raise serializers.ValidationError('Not allowed to delete category')
        if not BoardParticipant.objects.filter(
                board=value,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context['request'].user
        ).exists():
            raise serializers.ValidationError('You must be owner pr writer')
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')


# Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed deleted category')
        if value.user != self.context['request'].user:
            raise PermissionDenied
        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context['request'].user
        ).exists():
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
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

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
