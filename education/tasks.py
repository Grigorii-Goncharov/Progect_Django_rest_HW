from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta

from django.utils import timezone

from education.models import Course
from users.models import Subscription, User


@shared_task
def send_mail_update_course_notification(course_id):
    """Асинхронная отправка сообщения пользователю"""
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    subscribers = Subscription.objects.filter(
        course=course, is_active=True
    ).select_related("user")

    recipient_list = [sub.user.email for sub in subscribers if sub.user.email]

    if not recipient_list:
        return

    subject = f"Обновление курса: {course.title}"
    message = f"Курс '{course.title}' был обновлён. Посмотрите изменения!"
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    print(f"Deactivated {count} inactive users.")
