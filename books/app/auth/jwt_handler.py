from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

jwt = JWTManager()

def create_token(username):
    return create_access_token(identity=username)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username
