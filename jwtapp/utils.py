import jwt
import datetime
from configs import SECRET_KEY

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + datetime.timedelta(minutes=5),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

    print(access_token)

token = generate_access_token(1)
print(token)