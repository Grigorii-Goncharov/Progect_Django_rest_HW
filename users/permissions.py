from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    """Разрешает доступ следующим образом:
    - Администраторы (is_staff): полный доступ ко всем операциям.
    - Владельцы объекта: полный доступ к своему объекту.
    - Модераторы (пользователи в группе 'Moderator'):
        * Не могут создавать новые объекты (POST запрещён).
        * Могут просматривать (GET) и редактировать (PUT, PATCH) любые объекты.
        * Не могут удалять объекты (DELETE запрещён).
    - Остальные аутентифицированные пользователи:
        * Могут только просматривать (GET).
        * Не могут создавать, редактировать или удалять.
    - Неаутентифицированные пользователи: доступ запрещён.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return (
                request.user.is_authenticated
                and not request.user.groups.filter(name="Moderator").exists()
            )
        if request.method in ["GET"]:
            return request.user.is_authenticated
        return True  # PUT/PATCH/DELETE — проверяются в has_object_permission

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:  # Для Админа
            return True
        if obj.owner == request.user:
            return True
        if request.user.groups.filter(name="Moderator").exists():
            return request.method in ["GET", "PUT", "PATCH"]  # DELETE — запрещён!
        return False