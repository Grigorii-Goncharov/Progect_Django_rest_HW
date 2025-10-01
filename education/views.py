from rest_framework.permissions import IsAuthenticated
from education.models import Course, Lesson
from education.serializers import (
    CourseSerializer,
    CourseSerializerList,
    LessonSerializer,
)
from rest_framework import viewsets, generics
from users.permissions import IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Поддерживает все стандартные операции: создание, чтение, обновление и удаление.

    Права доступа:
    - Создание: только аутентифицированные пользователи (не модераторы).
    - Просмотр списка: все аутентифицированные пользователи.
      - Обычные пользователи видят только свои курсы.
      - Модераторы и администраторы видят все курсы.
    - Просмотр деталей, редактирование, удаление:
      - Владельцы курса — полный доступ.
      - Модераторы — могут просматривать и редактировать, но не удалять.
      - Администраторы — полный доступ.

    При создании курса автоматически устанавливается текущий пользователь как владелец.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия."""
        if self.action == "retrieve":
            return CourseSerializerList
        return CourseSerializer

    def get_queryset(self):
        """
        Возвращает queryset курсов в зависимости от роли пользователя:
        - Модераторы и администраторы видят все курсы.
        - Обычные пользователи видят только свои курсы.
        """
        if self.request.user.groups.filter(name="Moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя владельцем создаваемого курса."""
        serializer.save(owner=self.request.user)


class LessonCreateList(generics.ListCreateAPIView):
    """
    Представление для создания нового урока и получения списка уроков.

    Права доступа:
    - Создание: только аутентифицированные пользователи (не модераторы).
    - Просмотр списка:
      - Обычные пользователи видят только свои уроки.
      - Модераторы и администраторы видят все уроки.

    При создании урока автоматически устанавливается текущий пользователь как владелец.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя владельцем создаваемого урока."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от роли пользователя:
        - Модераторы и администраторы получают все уроки.
        - Обычные пользователи получают только свои уроки.
        """
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления отдельного урока.

    Права доступа:
    - Владельцы урока: полный доступ (просмотр, редактирование, удаление).
    - Модераторы: могут просматривать и редактировать, но не удалять.
    - Администраторы: полный доступ.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от роли пользователя:
        - Модераторы и администраторы получают все уроки.
        - Обычные пользователи получают только свои уроки.
        """
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
