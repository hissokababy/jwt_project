from jwtapp.models import Session
from django.contrib.auth.models import User

def update_token(user, token):
    session = Session.objects.filter(user=user).exists()

    # print(session.refresh_token)

    return True


def get_user(user_id):
    user = User.objects.filter(id=user_id).exists()

    if user == True:
        return user