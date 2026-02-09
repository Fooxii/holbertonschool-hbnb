import uuid
from datetime import datetime
from user import User


class Place:
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._title = None
        self._description = None
        self._price = None
        self._latitude = None
        self._longitude = None
        self._owner = None

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise TypeError("id must be a string")
        self._id = value
        self._touch()


    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if len(value) > 100:
            raise ValueError("title must be less than 100 characters long")
        if len(value.strip()) == 0:
            raise ValueError("title is required")

        self._title = value
        self._touch()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("description must be a string")
        self._description = value
        self._touch()


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError("price must be a float")
        if value <= 0:
            raise ValueError("price must be positive")
        self._price = value
        self._touch()


    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError("latitude must be a float")
        if value > 90.0 or value < -90.0:
            raise ValueError("latitude must not be greater than 90 or lesser than -90")
        self._latitude = value
        self._touch()


    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError("longitude must be a float")
        if value > 180.0 or value < -180.0:
            raise ValueError("longitude must not be greater than 180 or less than -180")
        self._longitude = value
        self._touch()


    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("owner must be a User instance")
        self._owner = value
        self._touch()


    def _touch(self):
        self._updated_at = datetime.now()
