from mongoengine import Document, StringField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    admin = BooleanField(default=False)

    def set_password(self, password):
        """Hashes the password and stores it in the password_hash field."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Checks if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)
