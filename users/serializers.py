from rest_framework.serializers import ModelSerializer
from users.models import Payment


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment (Платежи).
    Используется для преобразования данных модели Payment в JSON-формат и обратно.
    Поддерживает все поля модели, включая:
        - user: пользователь, совершивший платёж
        - payment_date: дата и время платежа
        - course: оплаченный курс (опционально)
        - lesson: оплаченный урок (опционально)
        - amount: сумма платежа
        - payment_method: способ оплаты
    """

    class Meta:
        model = Payment
        fields = "__all__"
