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


def edit_photo(validated_data):
    photo = Image.open(validated_data['photo'])
    quality = validated_data.get('quality')

    sizes = (1920, 1080)
    if photo.size < sizes:
        photo = photo.resize((1920, 1080))

    if not quality:
        quality = 80
    
    photo.format = 'webp'

    name = '.'.join(validated_data['photo'].name.split('.')[:-1]) + '.webp'

    thumb_io = BytesIO()
    photo.save(thumb_io, 'webp', quality=quality)
    avatar = files.File(thumb_io, name=name)
    return avatar
