from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # -------------------- USERS --------------------
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

    # -------------------- AMENITIES --------------------
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
        amenity.update(amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)
        return True

    # -------------------- PLACES --------------------
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.pop("owner_id"))
        if not owner:
            raise ValueError("Invalid owner_id")
        place = Place(owner=owner, **place_data)
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

        # Update owner if provided
        if "owner_id" in place_data:
            owner = self.user_repo.get(place_data.pop("owner_id"))
            if not owner:
                raise ValueError("Invalid owner_id")
            place.owner = owner

        # Update amenities if provided
        if "amenities" in place_data:
            amenity_ids = place_data.pop("amenities")
            place.amenities = []
            for a_id in amenity_ids:
                amenity = self.amenity_repo.get(a_id)
                if not amenity:
                    raise ValueError(f"Invalid amenity id: {a_id}")
                place.amenities.append(amenity)

        # Update other fields
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True

    # -------------------- REVIEWS --------------------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data.pop("user_id"))
        place = self.place_repo.get(review_data.pop("place_id"))
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")
        review = Review(author=user, place=place, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return []
        return place.reviews

    def get_reviews_by_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return []
        return user.reviews
    
    def get_review_by_user_and_place(self, user_id, place_id):
        reviews = self.review_repo.get_all()

        for review in reviews:
            if review.author.id == user_id and review.place.id == place_id:
                return review

        return None

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        # Update user or place if provided
        if "user_id" in review_data:
            user = self.user_repo.get(review_data.pop("user_id"))
            if not user:
                raise ValueError("Invalid user_id")
            review.author = user

        if "place_id" in review_data:
            place = self.place_repo.get(review_data.pop("place_id"))
            if not place:
                raise ValueError("Invalid place_id")
            review.place = place

        # Update other fields
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
