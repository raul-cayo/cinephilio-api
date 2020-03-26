from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('my_precious')
    return serializer.dumps(email, salt='my_precious_two')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('my_precious')
    try:
        email = serializer.loads(
            token,
            salt='my_precious_two',
            max_age=expiration
        )
    except:
        return False
    return email