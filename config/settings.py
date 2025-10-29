import sys
from datetime import timedelta
from pathlib import Path
import os

from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework_simplejwt",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "django_celery_beat",
    # 'corsheaders',
    "education",
    "users",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'corsheaders.middleware.CorsMiddleware',
]

# CORS_ALLOWED_ORIGINS = [
#     '<http://localhost:8000>',  # Замените на адрес вашего фронтенд-сервера
# ]
#
# CSRF_TRUSTED_ORIGINS = [
#     "https://read-and-write.example.com", #  Замените на адрес вашего фронтенд-сервера
#     # и добавьте адрес бэкенд-сервера
# ]

CORS_ALLOW_ALL_ORIGINS = False

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# if "docker-compose" in sys.argv[0]:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": os.getenv("DB_NAME"),
#             "USER": os.getenv("DB_USER"),
#             "PASSWORD": os.getenv("DB_PASSWORD"),
#             "HOST": os.getenv("DB_HOST"),
#             "PORT": os.getenv("DB_PORT"),
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": os.getenv("DB_NAME"),
#             "USER": os.getenv("DB_USER"),
#             "PASSWORD": os.getenv("DB_PASSWORD"),
#             "HOST": "localhost",
#             "PORT": os.getenv("DB_PORT"),
#         }
#     }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),  # "db" (имя сервиса docker-compose из .env)
        "PORT": os.getenv("DB_PORT"),
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
# STATICFILES_DIRS = (BASE_DIR / "static",)

STATICFILES_DIRS = [BASE_DIR / "static"]  # исходники статики
STATIC_ROOT = BASE_DIR / "staticfiles"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "users.User"  # ← указываем, что User — из приложения users

# LOGIN_REDIRECT_URL = 'users:profile'
# LOGOUT_REDIRECT_URL = 'catalog:home'
# LOGIN_URL = 'users:login'


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # Настройки почты
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("MAIL_HOST")
EMAIL_HOST_PASSWORD = os.getenv("MAIL_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}


# для теста
if "test" in sys.argv:
    ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

    # Дополнительные настройки для тестов
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",  # Быстрее для тестов
    ]


# Настройки Celery
# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Настройки Celery для работы с докером:
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0') # Используем REDIS_URL из окружения
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0') # Используем REDIS_URL из окружения


# Используем eventlet на Windows
CELERY_WORKER_POOL = "eventlet"
CELERY_WORKER_POOL_RESTARTS = True

# Опционально: сериализация
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "TIME_ZONE"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Настройки Celery Beat (планировщик)
CELERY_BEAT_SCHEDULE = {
    "deactivate-inactive-users-daily": {
        "task": "educations.tasks.deactivate_inactive_users",
        "schedule": crontab(hour=2, minute=0),  # каждый день в 02:00
    },
}
