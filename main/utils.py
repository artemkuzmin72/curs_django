from django.core.mail import send_mail
from django.utils import timezone
from .models import MailingAttempt

def send_mailing(mailing):
    """
    Отправка писем всем получателям рассылки с логированием каждой попытки.
    """
    subject = mailing.message.subject
    body = mailing.message.body
    recipients = mailing.recipients.all()

    if not recipients.exists():
        return "Нет получателей для рассылки."

    mailing.status = "started"
    mailing.save(update_fields=["status"])

    for recipient in recipients:
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False
            )
            # запись успешной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="success",
                server_response="Отправлено успешно"
            )
        except Exception as e:
            # запись неуспешной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="failed",
                server_response=str(e)
            )

    return f"Рассылка '{mailing.title}' завершена. Попыток: {recipients.count()}"