from django.core.mail import send_mail
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

    success_count = 0
    fail_count = 0

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
                status="Успешно",
                server_response="Отправлено успешно"
            )
            success_count += 1
        except Exception as e:
            # запись неуспешной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="Не успешно",
                server_response=str(e)
            )
            fail_count += 1

    mailing.status = "finished"
    mailing.save(update_fields=["status"])

    return f"Рассылка '{mailing.title}' завершена. Успешно: {success_count}, Неудачно: {fail_count}"