from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Ссылаем пользователя на группу'Модератор' с соответствующими правами"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderator').exists()
