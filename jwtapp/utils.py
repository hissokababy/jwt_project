from django.core.mail import send_mail

from project_jwt.settings import DEFAULT_FROM_EMAIL
from io import BytesIO
from django.core import files

from PIL import Image

def send_user_message(user, code):
    send_mail(
    "Subject here",
    f"Here is your code {code}",
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)


def edit_photo(photo: str, name: str, sizes: tuple=(1920, 1080), quality: int=80):

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
