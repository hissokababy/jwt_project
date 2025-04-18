from io import BytesIO
from django.core import files
from PIL import Image

from django.core.mail import send_mail
from jwtapp.models import User
from project_jwt.settings import DEFAULT_FROM_EMAIL


def send_user_message(user: User, code: int) -> None:
    send_mail(
    "Subject here",
    f"Here is your code {code}",
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)


def edit_photo(photo: str, name: str|None, sizes: tuple=(1920, 1080), quality: int=80) -> files.File:

    photo = Image.open(photo)

    if photo.size < sizes:
        photo = photo.resize(sizes)

    photo.format = 'webp'

    if not name:
        name = '.'.join(photo.name.split('.')[:-1]) + '.webp'
    else:
        name = '.'.join(name.split('.')[:-1]) + '.webp'

    thumb_io = BytesIO()
    photo.save(thumb_io, 'webp', quality=quality)
    avatar = files.File(thumb_io, name=name)
    return avatar
