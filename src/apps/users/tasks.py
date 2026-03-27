import smtplib
from email.message import EmailMessage

from loguru import logger
from pydantic import EmailStr

from src.celery.celery import celery_app
from src.settings.settings import settings


@celery_app.task(bind=True, max_retries=3, retry_backoff=True)
def send_welcome_email(self, email: EmailStr):
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = email
    message["Subject"] = "Добро пожаловать"
    message.set_content("Добро пожаловать в наш сервис!")

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()  # Enable encryption
            server.login(settings.SMTP_USER, settings.GMAIL_PASS)
            server.send_message(message)

            logger.info(f"Welcome email sent to {email}")

        return {
            "email": email,
            "message": "Письмо успешно отправлено",
        }
    except Exception as e:
        logger.exception(f"Error sending welcome email to {email}: {str(e)}")
        raise self.retry(exc=e, countdown=60 * (2**self.request.retries))
