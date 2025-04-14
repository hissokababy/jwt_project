from django.core.mail import send_mail

from jwtapp.models import User
from jwtapp.exeptions import DoesExsistUser
from project_jwt.settings import DEFAULT_FROM_EMAIL
from io import BytesIO

from PIL import Image

def send_user_message(user, code):
    send_mail(
    "Subject here",
    f"Here is your code {code}",
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)

from django.core import files

def change_user_photo(user_id, photo, width=1920, height=1080):
    try:
        user = User.objects.get(pk=user_id)
    except:
        raise DoesExsistUser

    img = Image.open(photo)
    resized = img.resize((width, height))
    resized.format = 'WebP'

    name = photo.name.split('.')[:-1][-1] + '.WebP'

    thumb_io = BytesIO()  # create a BytesIO object
    resized.save(thumb_io, 'WebP')
    avatar = files.File(thumb_io, name=name)

    user.avatar = avatar
    user.save()
