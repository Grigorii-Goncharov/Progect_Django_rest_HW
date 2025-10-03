from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from education.models import Course, Lesson
from education.validators import CorrectYoutubeVideoUrl
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson.
    Используется для преобразования экземпляров модели Lesson в JSON-формат
    и обратно. Включает все поля модели.
    Attributes:
        Meta.model (Lesson): Модель, с которой работает сериализатор.
        Meta.fields (str): "__all__" — включает все поля модели.
    """

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [CorrectYoutubeVideoUrl(field="video_url")]


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course с подсчётом количества уроков.
    Добавляет вычисляемое поле `count_lessons`, которое возвращает количество
    связанных уроков для каждого курса.
    Attributes:
        count_lessons (SerializerMethodField): Поле, вычисляемое методом `get_count_lessons`.
    Methods:
        get_count_lessons(subj): Возвращает количество уроков, связанных с курсом.
    Attributes:
        Meta.model (Course): Модель, с которой работает сериализатор.
        Meta.fields (str): "__all__" — включает все поля модели.
    """

    is_subscribed = serializers.SerializerMethodField()
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, subj):
        """
        Возвращает количество уроков, связанных с данным курсом.
        Args:
            subj (Course): Экземпляр модели Course.
        Returns:
            int: Количество связанных объектов Lesson.
        """
        return subj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializerList(ModelSerializer):
    """
    Расширенный сериализатор для модели Course, предназначенный для спискового отображения.
    Включает:
        - Основные поля курса: id, title, description, preview.
        - Вычисляемое поле `count_lessons` — количество уроков в курсе.
        - Вложенный список уроков через `LessonSerializer`.
        - Вычисляемое поле `is_subscribed` — указывает, подписан ли текущий пользователь на курс.

    Используется, когда требуется отобразить курс вместе с деталями его уроков и информацией
    о подписке текущего пользователя.
    Attributes:
        count_lessons (SerializerMethodField): Количество уроков в курсе.
            Значение вычисляется методом `get_count_lessons`.
        lessons (LessonSerializer): Сериализованный список связанных уроков (только для чтения).
        is_subscribed (SerializerMethodField): Флаг подписки текущего пользователя на курс.
            Значение вычисляется методом `get_is_subscribed`.
    Methods:
        get_count_lessons(obj): Возвращает количество уроков, связанных с курсом.
        get_is_subscribed(obj): Проверяет, подписан ли авторизованный пользователь на курс.
    Meta:
        model (Course): Модель, с которой работает сериализатор.
        fields (list): Список сериализуемых полей, включая вычисляемые и вложенные.
    """

    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # many = уроков может быть несколько(берем сериализатор урока)

    def get_count_lessons(self, subj):
        """
        Возвращает количество уроков, связанных с данным курсом.
        Args:
            subj (Course): Экземпляр модели Course.
        Returns:
            int: Количество связанных объектов Lesson.
        """
        return subj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=user, course=obj, is_active=True
        ).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "count_lessons",
            "lessons",
            "get_is_subscribed",
        ]
