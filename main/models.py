from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
    
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
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField(
        "Recipient", verbose_name="Получатели", blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- кастомный пользователь
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Автор',
        null=True  # если хочешь, чтобы существующие записи могли быть пустыми
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

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.mailing.title} — {self.status} ({self.timestamp.strftime('%d.%m.%Y %H:%M:%S')})"