from django.template.context_processors import request
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from education.models import Course

from users.models import Payment, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, UserProfileSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    Предоставляет полный набор операций CRUD для модели Payment.
    Поддерживает фильтрацию и сортировку через query-параметры.
    Доступные фильтры:
        - ?course=<id> — фильтр по курсу
        - ?lesson=<id> — фильтр по уроку
        - ?payment_method=cash|transfer — фильтр по способу оплаты
    Доступные сортировки:
        - ?ordering=payment_date — по дате (по умолчанию)
        - ?ordering=-payment_date — по дате в обратном порядке
    Примеры запросов:
        GET /api/payments/ — список всех платежей
        GET /api/payments/?course=1&ordering=-payment_date — платежи за курс 1, отсортированные по убыванию даты
        GET /api//users/payment/?payment_method=transfer - фильтрация (можно не указывать поле filterset)
    Используемый сериализатор: PaymentSerializer
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]


class UserCreateAPIview(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):  # ← ИСПРАВЛЕНО: ListAPIView!
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserSubscribeAPIView(APIView):
    """API для управления подпиской пользователя на курс: подписаться/отписаться
    работает только с теми методами, которые переопределены"""
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        user = request.user
        # Лучше передавать data в body, а не в GET(используется при POST, PUT, PATCH с форматами: JSON, form-data, etc.)
        # Передача числа курса в теле запроса(request - тело словарь(data), course_id - ключ)
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать 'course_id' в теле запроса."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            return Response(
                {"error": "Некорректный ID курса."},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subscription = Subscription.objects.filter(user=user, course=course).first()

        if subscription:
            if subscription.is_active:
                subscription.deactivate()
                message = "Подписка деактивирована"
            else:
                subscription.activate()
                message = "Подписка активирована"
        else:
            Subscription.objects.create(user=user, course=course, is_active=True)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
