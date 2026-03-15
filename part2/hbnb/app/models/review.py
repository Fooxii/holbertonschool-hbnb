from app import db
from .baseclass import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating):
        self.text = text
        self.rating = rating

    # ---------- VALIDATION ----------
    @validates("text")
    def validate_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        if len(value.strip()) == 0:
            raise ValueError("text is required")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    # ---------- UPDATE ----------
    def update(self, data: dict):
        allowed_fields = ["text", "rating"]
        for key, value in data.items():
            if key in allowed_fields:
                setattr(self, key, value)
