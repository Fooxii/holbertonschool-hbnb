import uuid
import re
from datetime import datetime


class User:
    def __init__(self, id, first_name, last_name, email, is_admin=False):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._first_name = None
        self._last_name = None
        self._email = None
        self._is_admin = is_admin
        self._places = []
        self._reviews = []



        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

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
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")
        if len(value) > 50:
            raise ValueError("first_name must be less than 50 characters long")
        if len(value.strip()) == 0:
            raise ValueError("first_name is required")
        self._first_name = value
        self._touch()


    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise TypeError("last_name must be a string")
        if len(value) > 50:
            raise ValueError("last_name must be less than 50 characters long")
        if len(value.strip()) == 0:
            raise ValueError("last_name is required")
        self._last_name = value
        self._touch()


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise TypeError("email must be a string")
        if not self._valid_email(value):
            raise ValueError("Invalid email format")
        if len(value.strip()) == 0:
            raise ValueError("email is required")
        self._email = value
        self._touch()


    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        self._is_admin = value
        self._touch()


    @property
    def places(self):
        return self._places

    def add_place(self, place):
        from place import Place
        if not isinstance(place, Place):
            raise TypeError("place must be an instance of the Place class")
        self._places.append(place)


    @property
    def reviews(self):
        return self._reviews

    def add_review(self, review):
        from review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be an instance of the Review class")
        self._reviews.append(review)


    def _touch(self):
        self._updated_at = datetime.now()

    def _valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)
