from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from config import settings



class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователя для работы с электронной почтой как с уникальным идентификатором.
    Позволяет создавать обычных пользователей и суперпользователей через email,
    без использования поля username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанным email и паролем.
        Args:
            email (str): Электронная почта пользователя (обязательное поле).
            password (str, optional): Пароль пользователя. Если не указан — пароль не устанавливается.
            **extra_fields: Дополнительные поля модели (например, phone, city и т.д.).
        Returns:
            User: Экземпляр созданного пользователя.
        Raises:
            ValueError: Если email не указан.
        """
        if not email:
            raise ValueError("Электронная почта является обязательным полем.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с правами администратора.
        Args:
            email (str): Электронная почта суперпользователя.
            password (str, optional): Пароль суперпользователя.
            **extra_fields: Дополнительные поля модели.
        Returns:
            User: Экземпляр созданного суперпользователя.
        Raises:
            ValueError: Если is_staff или is_superuser не установлены в True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя, использующая email вместо username для аутентификации.
    Добавляет дополнительные поля: телефон, город и аватарка.
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Уникальный адрес электронной почты, используемый для входа.",
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Телефон должен быть в формате: '+999999999'. До 15 цифр.",
            )
        ],
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Номер телефона в международном формате (например, +79991234567).",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Город проживания пользователя.",
    )
    avatar = models.ImageField(
        upload_to="user_avatars/",
        blank=True,
        null=True,
        verbose_name="Аватарка",
        help_text="Изображение профиля пользователя. Поддерживаются JPG, PNG.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Определяет, может ли пользователь войти в систему.",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Персонал",
        help_text="Определяет, имеет ли пользователь доступ к административной панели.",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
        help_text="Дата и время создания учетной записи.",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = (
        "email"  # Используем email как основной идентификатор для аутентификации
    )
    REQUIRED_FIELDS = (
        []
    )  # Не требует дополнительных полей при создании суперпользователя

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]  # По умолчанию сортировка по email

    def __str__(self):
        """
        Возвращает строковое представление пользователя — его email.
        Returns:
            str: Email пользователя.
        """
        return self.email


class Payment(models.Model):
    """
    Модель для хранения информации о платежах пользователей за курсы или уроки.
    Каждый платёж привязан к пользователю и может быть связан либо с курсом, либо с уроком (но не с обоими одновременно).
    Поддерживает фиксацию суммы, способа оплаты и даты совершения платежа.
    Поля:
        user (ForeignKey): Пользователь, совершивший платёж.
        payment_date (DateTimeField): Дата и время создания платежа (устанавливается автоматически).
        course (ForeignKey): Оплаченный курс (необязательно, взаимоисключающе с lesson).
        lesson (ForeignKey): Оплаченный урок (необязательно, взаимоисключающе с course).
        amount (DecimalField): Сумма платежа с точностью до двух знаков после запятой.
        payment_method (CharField): Способ оплаты — наличные или перевод на счёт.
    Валидация:
        - Должен быть указан либо курс, либо урок.
        - Нельзя указать и курс, и урок одновременно
    """

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        "education.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    lesson = models.ForeignKey(
        "education.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",  # DecimalField - поле для денег вместо float
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        """
        Возвращает человекочитаемое строковое представление платежа.
        Формат: "Платеж {сумма} от {пользователь} за {название курса/урока}".
        Если ни курс, ни урок не указаны — подставляется "Не указано".
        """
        paid_item = (
            self.course.title
            if self.course
            else (self.lesson.title if self.lesson else "Не указано")
        )
        return f"Платеж {self.amount} от {self.user} за {paid_item}"

    def clean(self):
        """
         Выполняет валидацию бизнес-логики модели перед сохранением.
        Правила:
        - Должен быть указан хотя бы один из объектов: курс или урок.
        - Нельзя указать и курс, и урок одновременно — это взаимоисключающие поля.
        Raises:
        ValidationError: если правила нарушены.
        """
        if not self.course and not self.lesson:
            raise ValidationError("Должен быть указан хотя бы один: курс или урок.")
        if self.course and self.lesson:
            raise ValidationError(
                "Нельзя одновременно указать и курс, и урок. Выберите что-то одно."
            )

    def save(self, *args, **kwargs):
        """
        Переопределённый метод сохранения, вызывающий полную валидацию перед записью в БД.
        Используется для обеспечения целостности данных: перед сохранением вызывается self.full_clean(),
        что, в свою очередь, вызывает метод clean().
        Args:
            *args: стандартные аргументы Model.save().
            **kwargs: стандартные именованные аргументы Model.save().
        Raises:
            ValidationError: если валидация не пройдена.
        """
        self.full_clean()  # вызываем валидацию перед сохранением
        super().save(*args, **kwargs)



class Subscription(models.Model):
    """
    Модель подписки пользователя на обновления курса.
    Позволяет отслеживать, за какими курсами следит пользователь,
    чтобы уведомлять его о новых материалах, изменениях или обновлениях.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions"
    )
    course = models.ForeignKey(
        "education.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscribers"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Указывает, активна ли подписка. Неактивные подписки не получают уведомлений."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания подписки."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего изменения подписки."
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")  # Один пользователь может быть подписан на курс только один раз
        ordering = ["-created_at"]

    def __str__(self):
        status = "активна" if self.is_active else "неактивна"
        return f"Подписка {self.user} на курс '{self.course}' ({status})"

    def deactivate(self):
        """Метод для деактивации подписки без её удаления."""
        self.is_active = False
        self.save()

    def activate(self):
        """Метод для повторной активации подписки."""
        self.is_active = True
        self.save()

