from project_jwt.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

def send_user_message() -> None:
    send_mail(
    "Subject here",
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=['receiver@gmail.com'],
    fail_silently=False,
)