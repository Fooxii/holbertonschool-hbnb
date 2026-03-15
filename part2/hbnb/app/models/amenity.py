from app import db
from .baseclass import BaseModel
from sqlalchemy.orm import relationship, validates

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(100), nullable=False)
    places = relationship("Place", secondary="place_amenity", back_populates="amenities")

    def __init__(self, name):
        self.name = name

    # ---------- VALIDATION ----------
    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be less than 50 characters long")
        return value

    # ---------- UPDATE ----------
    def update(self, data: dict):
        allowed_fields = ["name"]
        for key, value in data.items():
            setattr(self, key, value)
