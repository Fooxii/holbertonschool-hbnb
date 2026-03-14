from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None

        user.update(data)
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False

        self.user_repo.delete(user_id)
        return True


    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False

        self.amenity_repo.delete(amenity_id)
        return True


    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Invalid owner")

        amenities = []
        for amenity_id in place_data['amenities']:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Invalid amenity")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        for amenity in amenities:
            place.add_amenities(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'amenities' in place_data:
            place._amenities = []  # reset
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity")
                place.add_amenities(amenity)
            place_data.pop('amenities')

        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Invalid owner")
            place.owner = owner
            place_data.pop('owner_id')

        for key, value in place_data.items():
            setattr(place, key, value)

        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False

        self.place_repo.delete(place_id)
        return True


    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            raise ValueError("Invalid user or place")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            setattr(review, key, value)

        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True
