from rest_framework import permissions

from goals.models import BoardParticipant

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user_id == request.user.id


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        filters: dict = {'user': request.user, 'board': obj}
        if not request.user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**filters).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        filters: dict = {'user': request.user, 'board': obj.board}
        if not request.user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()
