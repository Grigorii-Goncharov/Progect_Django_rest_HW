from django.urls import path

from .apps import EducationConfig
from rest_framework.routers import DefaultRouter

from .models import Lesson
from .serializers import LessonSerializer
from .views import CourseViewSet, LessonCreateList, LessonRetrieveUpdateDestroy

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

app_name = EducationConfig.name

urlpatterns = [
    path(
        "lesson/",
        LessonCreateList.as_view(
            queryset=Lesson.objects.all(), serializer_class=LessonSerializer
        ),
        name="lesson-list",
    ),
    path(
        "lesson/<int:pk>/",
        LessonRetrieveUpdateDestroy.as_view(
            queryset=Lesson.objects.all(), serializer_class=LessonSerializer
        ),
        name="lesson-update",
    ),
]

urlpatterns += router.urls
