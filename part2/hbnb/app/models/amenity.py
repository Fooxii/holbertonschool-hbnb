from app import db
from .baseclass import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    # ---------- VALIDATION ----------
    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        value = value.strip()
        if len(value) == 0:
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be less than 50 characters long")
        return value

    # ---------- UPDATE ----------
    def update(self, data: dict):
        allowed_fields = ["name"]
        for key, value in data.items():
            if key in allowed_fields:
                setattr(self, key, value)
