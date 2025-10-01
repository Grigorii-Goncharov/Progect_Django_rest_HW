from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from education.models import Course, Lesson


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
    Используется, когда нужно отобразить курс вместе с деталями его уроков.
    Attributes:
        count_lessons (SerializerMethodField): Поле, вычисляемое методом `get_count_lessons`.
        lessons (LessonSerializer): Вложенный сериализатор для отображения связанных уроков.
    Methods:
        get_count_lessons(subj): Возвращает количество уроков, связанных с курсом.
    Attributes:
        Meta.model (Course): Модель, с которой работает сериализатор.
        Meta.fields (list): Явный список полей для сериализации.
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

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "count_lessons",
            "lessons",
        ]
