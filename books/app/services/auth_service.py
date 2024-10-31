from models.user import User
from auth.jwt_handler import create_token

def register_user(username, password, admin=False):
    user = User(username=username, admin=admin)
    user.set_password(password)
    user.save()
    return user

def login_user(username, password):
    user = User.objects(username=username).first()
    if user and user.check_password(password):
        return create_token(user.username)
    return None
