FROM python:3.12-slim

# Устанавливаем системные зависимости для компиляции пакетов из документации
#каждой отдельной зависимости для установки через Debian/Ubuntu
RUN apt-get update && pip install poetry

# Рабочая директория
WORKDIR /Progect_Django_rest_HW

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Настраиваем Poetry и устанавливаем зависимости
# --no-root: не устанавливаем сам проект как пакет (опционально, но безопасно)
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Копируем исходный код
COPY . .

# Создаём папку media (на случай, если том не смонтирован)
RUN mkdir -p /Progect_Django_rest_HW/media

# Открываем порт (для документации, не обязателен)
EXPOSE 8000

# Запуск приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
