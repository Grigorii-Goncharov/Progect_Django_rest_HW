from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator


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
            raise ValueError('Электронная почта является обязательным полем.')
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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя Django, использующая email вместо username для аутентификации.
    Добавляет дополнительные поля: телефон, город и аватарка.
    Поддерживает стандартную систему разрешений Django (PermissionsMixin).
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Уникальный адрес электронной почты, используемый для входа."
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Телефон должен быть в формате: '+999999999'. До 15 цифр."
            )
        ],
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Номер телефона в международном формате (например, +79991234567)."
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Город проживания пользователя."
    )
    avatar = models.ImageField(
        upload_to='user_avatars/',
        blank=True,
        null=True,
        verbose_name="Аватарка",
        help_text="Изображение профиля пользователя. Поддерживаются JPG, PNG."
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Определяет, может ли пользователь войти в систему."
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Персонал",
        help_text="Определяет, имеет ли пользователь доступ к административной панели."
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
        help_text="Дата и время создания учетной записи."
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Используем email как основной идентификатор для аутентификации
    REQUIRED_FIELDS = []  # Не требует дополнительных полей при создании суперпользователя

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['email']  # По умолчанию сортировка по email

    def __str__(self):
        """
        Возвращает строковое представление пользователя — его email.
        Returns:
            str: Email пользователя.
        """
        return self.email
