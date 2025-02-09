from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
)

async def send_reset_email(email:str, reset_token: str):
    reset_link = f"http://127.0.0.1:8000/users/reset-password?token={reset_token}"

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body= f"""
                Hello,

                You requested a password reset. Click the link below to reset your password:

                {reset_link}

                If you didn't request this, please ignore this email.

                Regards,
                FastAPI Auth System
                """,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)