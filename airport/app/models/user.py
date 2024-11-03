from mongoengine import Document, StringField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    """
    A class to represent a user in the system.

    Attributes:
    ----------
    username : StringField
        A unique and required string field for the user's username.
    password_hash : StringField
        A required string field to store the hashed password of the user.
    admin : BooleanField
        A boolean field to indicate if the user has admin privileges, defaults to False.
    """
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    admin = BooleanField(default=False)

    def set_password(self, password):
        """
        Hashes the password and stores it in the password_hash field.

        Parameters:
        ----------
        password : str
            The plain text password to be hashed and stored.
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Checks if the provided password matches the stored password hash.

        Parameters:
        ----------
        password : str
            The plain text password to be checked against the stored hash.

        Returns:
        -------
        bool
            True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
