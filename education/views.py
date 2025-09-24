from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson
from education.serializers import CourseSerializer, CourseSerializerList, LessonSerializer

from rest_framework import viewsets, generics

from users.permissions import IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для вывода списка курсов и информации по одному объекту
    ModelViewSet - достаточен для передачи queryset и serializer и все работает из коробки
    """

    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_serializer_class(self):
        """Метод ловит действие 'retrieve', то перенаправляет на другой сериализатор"""
        if self.action == "retrieve":
            return CourseSerializerList
        return CourseSerializer

    def get_queryset(self):
        """Кто может смотреть все уроки или только свои"""
        if self.request.user.groups.filter(name='Moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Автоприсваиание автора - владельца"""
        serializer.save(owner=self.request.user)


class LessonCreateList(generics.ListCreateAPIView):
    """Viewset для создания и просмотра урока или списков урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]# Распределение прав пользователя и модератора

    def perform_create(self, serializer):
        """Автоприсваиание автора - владельца"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Кто может смотреть все курсы или только свои"""
        if self.request.user.groups.filter(name='Moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Viewset для обновления и удаления урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]

    def get_queryset(self):
        """Кто может смотреть все уроки или только свои"""
        if self.request.user.groups.filter(name='Moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

