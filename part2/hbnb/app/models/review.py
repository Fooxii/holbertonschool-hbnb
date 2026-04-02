from app import db
from .baseclass import BaseModel
from sqlalchemy.orm import relationship, validates

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    # Relationships
    author = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")

    def __init__(self, text, rating, author, place):
        self.text = text
        self.rating = rating
        self.author = author
        self.place = place

    # ---------- VALIDATION ----------
    @validates("text")
    def validate_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        value = value.strip()
        if not value:
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
        allowed_fields = ["text", "rating", "author", "place"]
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,

            "author_name": self.author.email if self.author and hasattr(self.author, "email") else "Anonymous"
        }
