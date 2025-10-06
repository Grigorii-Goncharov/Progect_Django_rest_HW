from django.urls import path

from users.views import PayCourseAPIView, PayLessonAPIView
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

    # покупка курса и урока
    path('course/<int:course_id>/pay/', PayCourseAPIView.as_view(), name='course-pay'),
    path('lesson/<int:lesson_id>/pay/', PayLessonAPIView.as_view(), name='lesson-pay'),

]

urlpatterns += router.urls
