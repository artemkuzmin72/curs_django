from django.db import models
from django.conf import settings

class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название рассылки")
    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    is_active = models.BooleanField(default=True)
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )

    message = models.ForeignKey('main.Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField('main.Recipient', verbose_name="Получатели", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Автор',
        null=True
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    mailing = models.ForeignKey(
        "Mailing",
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ответ почтового сервера"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-timestamp"]