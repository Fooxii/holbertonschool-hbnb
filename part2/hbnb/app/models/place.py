from app import db
from .baseclass import BaseModel
from sqlalchemy.orm import validates


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, title, price, latitude, longitude, description=None):
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.description = description

    # ---------- VALIDATION ----------
    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if len(value.strip()) == 0:
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be less than 100 characters long")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("description must be a string")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError("price must be a float")
        if value <= 0:
            raise ValueError("price must be positive")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise TypeError("latitude must be a float")
            if value < -90 or value > 90:
                raise ValueError("latitude must be between -90 and 90")
        return value

    @validates("longitude")
    def validate_longitude(self, key, value):
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise TypeError("longitude must be a float")
            if value < -180 or value > 180:
                raise ValueError("longitude must be between -180 and 180")
        return value

    # ---------- UPDATE ----------
    def update(self, data: dict):
        allowed_fields = ["title", "description", "price", "latitude", "longitude"]
        for key, value in data.items():
            if key in allowed_fields:
                setattr(self, key, value)
