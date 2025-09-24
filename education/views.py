from django.shortcuts import get_object_or_404
from education.models import Course, Lesson
from education.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseSerializerList,
)
from rest_framework import viewsets, status, generics
from rest_framework.response import Response


class CourseViewSet(viewsets.ViewSet):
    """
    ViewSet для управления курсами (Course).
    Реализует стандартные CRUD-операции через HTTP-методы:
    - GET /courses/       — получение списка всех курсов
    - POST /courses/      — создание нового курса
    - GET /courses/{id}/  — получение одного курса по ID
    - PUT /courses/{id}/  — полное обновление курса
    - PATCH /courses/{id}/ — частичное обновление курса
    - DELETE /courses/{id}/ — удаление курса
    Использует CourseSerializer для сериализации/десериализации данных.
    Все ответы возвращаются в формате JSON с корректными HTTP-статусами.
    """

    def list(self, request):
        """
        Возвращает список всех курсов.
        Метод: GET /courses/
        """
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Создаёт новый курс на основе переданных данных.
        Метод: POST /courses/
        Ожидаемые данные:
            JSON-объект с полями, соответствующими модели Course (например, title, description, etc.).
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную информацию о курсе по его уникальному идентификатору.
        Метод: GET /courses/{id}/
        Аргументы:
            pk (str): Уникальный идентификатор курса (первичный ключ).
        Возвращает:
            Response: Сериализованные данные курса с использованием CourseSerializerList.
        """
        course = get_object_or_404(Course.objects.all(), pk=pk)
        serializer = CourseSerializerList(
            course
        )  # или CourseSerializer, если нужен детальный
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Полностью обновляет существующий курс.
        Метод: PUT /courses/{id}/
        Заменяет все поля курса на переданные в запросе.
        Если поле не передано — оно будет установлено в null/пустое значение.
        Аргументы:
            pk (str): Уникальный идентификатор курса.
        """
        course = get_object_or_404(Course.objects.all(), pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Частично обновляет существующий курс.
        Метод: PATCH /courses/{id}/
        Обновляет только те поля, которые переданы в теле запроса.
        Остальные поля остаются без изменений.
        Аргументы:
            pk (str): Уникальный идентификатор курса.
        """
        course = get_object_or_404(Course.objects.all(), pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаляет курс по его ID.
        Метод: DELETE /courses/{id}/
        После удаления курс больше не доступен. Возвращает пустой ответ.
        Аргументы:
            pk (str): Уникальный идентификатор курса.
        """
        course = get_object_or_404(Course.objects.all(), pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonCreateList(generics.ListCreateAPIView):
    """
    API-эндпоинт для просмотра списка уроков и создания нового урока.
    Поддерживает два HTTP-метода:
        - GET: Получить список всех уроков.
        - POST: Создать новый урок, отправив данные в теле запроса.
    Использует LessonSerializer для преобразования данных между моделью и JSON.
    Примеры:
        GET     /lessons/      → Вернёт массив всех уроков.
        POST    /lessons/      → Создаст урок из переданных данных.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()




class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API-эндпоинт для просмотра, полного или частичного обновления и удаления одного урока.
    Поддерживает три HTTP-метода:
        - GET: Получить детальную информацию об уроке по его ID.
        - PUT/PATCH: Обновить урок полностью (PUT) или частично (PATCH).
        - DELETE: Удалить урок.
    Использует LessonSerializer для сериализации данных.
    Примеры:
        GET     /lessons/{id}/       → Получить урок.
        PUT     /lessons/{id}/       → Полностью заменить урок.
        PATCH   /lessons/{id}/       → Обновить только указанные поля.
        DELETE  /lessons/{id}/       → Удалить урок.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
