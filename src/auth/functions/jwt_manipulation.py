import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
import datetime

SECRET_KEY = 'super_segreto_shhhh'

def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600),  # Token expires in 1 hour
        "iat": datetime.datetime.now(datetime.timezone.utc)
    }

    print(f"Expiration: {payload["exp"]}")
    print(f"Issued At: {payload["iat"]}")

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=['HS256', ]
        )
        return payload
    except ExpiredSignatureError as error:
        return 2
    except InvalidSignatureError as error:
        return 1
    except Exception as error:
        print(error)
        return  0