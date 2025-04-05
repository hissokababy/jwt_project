from jwtapp.models import RefreshToken, Session
from django.contrib.auth.models import User

def user_sessions(user, token):
    get_user_sessions = Session.objects.filter(user=user.id)

    if not len(get_user_sessions) > 3 and user.is_active != False:
        session = Session.objects.create(user=user)

        refresh_token = RefreshToken.objects.create(session=session, token=token)

        return True


