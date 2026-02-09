import uuid
from datetime import datetime


class Amenity:
    def __init__(self, name):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._name = None

        self.name = name


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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be less than 50 characters long")
        self._name = value
        self._touch()


    def _touch(self):
        self._updated_at = datetime.now()
