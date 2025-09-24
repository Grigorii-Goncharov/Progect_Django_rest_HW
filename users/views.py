from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_object(self):
        return self.request.user  # Всегда возвращает текущего пользователя


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
