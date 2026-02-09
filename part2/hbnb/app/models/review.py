import uuid
from datetime import datetime
from user import User
from place import Place


class Review:
    def __init__(self, text, rating, place, user):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._text = None
        self._rating = None
        self._place = None
        self._user = None

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user


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
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        if len(value.strip()) == 0:
            raise ValueError("text is required")
        self._text = value
        self._touch()


    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        self._rating = value
        self._touch()


    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("place must be an instance of the Place class")
        self._place = value
        value.add_review(self)
        self._touch()


    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("user must be an instance of the User class")
        self._user = value
        value.add_review(self)
        self._touch()


    def _touch(self):
        self._updated_at = datetime.now()
