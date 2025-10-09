from rest_framework.serializers import ModelSerializer
from users.models import Payment, User, Subscription


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment (Платёж).
    Предназначен для преобразования экземпляров модели Payment в JSON-представление
    и обратно. Включает все поля модели:
        - user: пользователь, совершивший платёж;
        - payment_date: дата и время совершения платежа;
        - course: курс, за который произведён платёж (может быть null);
        - lesson: урок, за который произведён платёж (может быть null);
        - amount: сумма платежа;
        - payment_method: способ оплаты (например, 'cash' или 'transfer').
    """

    class Meta:
        model = Payment
        fields = ["id", "user", "course", "lesson", "amount", "payment_method", "payment_date", "stripe_session_id"]
        read_only_fields = ["id", "user", "payment_date"]


class UserSerializer(ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя.
    Используется при редактировании пользовательских данных, включая смену пароля.
    Поля:
        - username, email, first_name, last_name: общедоступные данные профиля;
        - password: пароль (только для записи, не возвращается в ответах API).
    При обновлении пароля он хэшируется с помощью метода set_password().
    """

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для просмотра публичного профиля пользователя.
    Предоставляет только базовую информацию о пользователе:
        - username
        - email
        - first_name
        - last_name
    Все поля доступны только для чтения — изменение через этот сериализатор невозможно.
    """

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        read_only_fields = fields


class SubscribeSerializer(ModelSerializer):
    """Сериализатор модели 'Подписки'"""

    class Meta:
        model = Subscription
        fields = "__all__"


