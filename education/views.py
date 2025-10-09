from rest_framework.permissions import IsAuthenticated
from education.models import Course, Lesson
from education.paginators import MyPagination
from education.serializers import (
    CourseSerializer,
    CourseSerializerList,
    LessonSerializer,
)
from rest_framework import viewsets, generics
from users.permissions import IsOwnerOrModerator
from education.tasks import send_mail_update_course_notification


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

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = MyPagination

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
        if (
            self.request.user.is_staff
            or self.request.user.groups.filter(name="Moderator").exists()
        ):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя владельцем создаваемого курса."""
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # важно для доступа к user
        return context

    def perform_update(self, serializer):
        """При методе PUT или PATCH срабатывает task на отправку сообщения при изменении курса"""
        course = serializer.save()
        send_mail_update_course_notification.delay(course.id)


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

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя владельцем создаваемого урока."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от роли пользователя:
        - Модераторы и администраторы получают все уроки.
        - Обычные пользователи получают только свои уроки.
        """
        if (
            self.request.user.is_staff
            or self.request.user.groups.filter(name="Moderator").exists()
        ):
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

    queryset = Lesson.objects.all()  # ← ВСЕ объекты!
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # ← главный пермишен

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от роли пользователя:
        - Модераторы и администраторы получают все уроки.
        - Обычные пользователи получают только свои уроки.
        """
        user = self.request.user
        if user.is_staff or user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)
