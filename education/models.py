from django.db import models

from users.models import User


class Course(models.Model):
    """
    Модель, представляющая обучающий курс.
    Курс содержит название, описание и превью-изображение.
    Связан с множеством уроков через отношение "один ко многим".
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Краткое название курса (до 200 символов).",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание содержания и целей курса.",
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Изображение-превью для отображения в списке курсов. Поддерживаются JPG, PNG.",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_course",
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Владелец, к которому относится этот курс. При удалении круса — курсы удаляются.",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        """
        Возвращает строковое представление курса — его название.
        Returns:
            str: Название курса.
        """
        return self.title


class Lesson(models.Model):
    """
    Модель, представляющая отдельный урок внутри курса.
    Урок связан с одним курсом (ForeignKey) и содержит название,
    описание, превью и ссылку на видео-материал.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Краткое название урока (до 200 символов).",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Краткое описание содержания урока, задачи или темы.",
    )
    preview = models.ImageField(
        upload_to="lesson_previews/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Изображение-превью для урока. Отображается в списке уроков.",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Полный URL на видео (YouTube, Vimeo, или другой хостинг).",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Курс, к которому относится этот урок. При удалении урока — уроки удаляются.",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_lesson",
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Владелец, к которому относится этот урок. При удалении урока — уроки удаляются.",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]  # Уроки автоматически сортируются по порядку создания

    def __str__(self):
        """
        Возвращает строковое представление урока в формате: "Название урока (Название курса)".
        Returns:
            str: Строка вида "{title} ({course.title})"
        """
        return f"{self.title} ({self.course.title})"
