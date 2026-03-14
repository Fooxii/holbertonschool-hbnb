import re
from app import db, bcrypt
from .baseclass import BaseModel
from sqlalchemy.orm import validates


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    # ---------- VALIDATION ----------

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be less than 50 characters long")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("last_name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be less than 50 characters long")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        if len(value.strip()) == 0:
            raise ValueError("email is required")

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        return value

    @validates("is_admin")
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    # ---------- PASSWORD ----------

    def hash_password(self, password):
        if not isinstance(password, str) or len(password.strip()) == 0:
            raise ValueError("Password must be a non-empty string")

        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # ---------- UPDATE ----------

    def update(self, data: dict):
        allowed_fields = ["first_name", "last_name", "email", "is_admin"]

        for key, value in data.items():
            if key == "password":
                self.hash_password(value)
            elif key in allowed_fields:
                setattr(self, key, value)
