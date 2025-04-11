from django.core.mail import send_mail

from project_jwt.settings import DEFAULT_FROM_EMAIL


def send_mail_to_user(user, code):
    send_mail(
    "Subject here",
    f"Here is your code {code}",
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)