from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from education.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializerList(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # many = уроков может быть несколько(берем сериализатор урока)

    def get_count_lessons(self, subj):
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
