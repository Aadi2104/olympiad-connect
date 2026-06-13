from fastapi_mail import FastMail, ConnectionConfig,MessageSchema, MessageType
from app.core.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS =settings.MAIL_SSL_TLS
)

mail = FastMail(
    config=mail_config)

def create_message(subject:str,recipients:list,body):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html
        )
        return message
    
