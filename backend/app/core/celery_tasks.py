from celery import shared_task
import smtplib
from email.message import EmailMessage
from .celery_config import celery_app
from ..core.config import settings


@celery_app.task(name='backend.app.core.celery_tasks.send_booking_code')
def send_booking_code(
    to_email: str,
    booking_code: str,
):
    text = f"Ваш код бронирования: {booking_code}"

    msg = EmailMessage()
    msg["Subject"] = "Подтверждение бронирования"
    msg["From"] = settings.email.email_username
    msg["To"] = to_email
    msg.set_content(text)

    with smtplib.SMTP_SSL(
        settings.email.email_host,
        settings.email.email_port
    ) as smtp:
        smtp.login(
            settings.email.email_username,
            settings.email.email_password.get_secret_value()
        )
        smtp.send_message(msg)