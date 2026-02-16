import unittest
import uuid
from app import create_app

class TestValidationEndpoints(unittest.TestCase):
    def setUp(self):
        # Create Flask app and test client
        self.app = create_app()
        self.client = self.app.test_client()

        # Generate a unique email for the test user
        unique_email = f"jane.doe.{uuid.uuid4().hex}@example.com"

        # Create a new user for each test
        user_payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        }

        user_resp = self.client.post("/api/v1/users/", json=user_payload)
        if user_resp.status_code != 201:
            raise RuntimeError(f"User creation failed: {user_resp.get_json()}")
        
        self.user_id = user_resp.get_json()["id"]

    # -------------------------
    # User tests
    # -------------------------
    def test_create_user_valid(self):
        payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": f"alice.smith.{uuid.uuid4().hex}@example.com"
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], payload["first_name"])
        self.assertEqual(data["last_name"], payload["last_name"])
        self.assertEqual(data["email"], payload["email"])

    def test_create_user_invalid_email(self):
        payload = {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "invalid-email"
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_create_user_empty_fields(self):
        payload = {
            "first_name": "",
            "last_name": "",
            "email": ""
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    # -------------------------
    # Place tests
    # -------------------------
    def test_create_place_valid(self):
        payload = {
            "title": "Cozy Cottage",
            "description": "Nice place to stay",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id,
            "amenities": []
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)

    def test_create_place_invalid_price(self):
        payload = {
            "title": "Cheap Shack",
            "description": "Not great",
            "price": "free",
            "latitude": 40.0,
            "longitude": -74.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_create_place_invalid_longitude(self):
        payload = {
            "title": "Beach House",
            "description": "Lovely view",
            "price": 250.0,
            "latitude": 25.0,
            "longitude": "far-east",
            "owner_id": self.user_id,
            "amenities": []
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    # -------------------------
    # Review tests
    # -------------------------
    def test_create_review_valid(self):
        # First, create a place
        place_payload = {
            "title": "Mountain Cabin",
            "description": "Cozy cabin",
            "price": 200.0,
            "latitude": 35.0,
            "longitude": -120.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_resp = self.client.post("/api/v1/places/", json=place_payload)
        place_id = place_resp.get_json()["id"]

        review_payload = {
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": place_id
        }
        resp = self.client.post(f"/api/v1/reviews/", json=review_payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)

    def test_create_review_invalid_place(self):
        review_payload = {
            "text": "Bad place",
            "rating": 1,
            "user_id": self.user_id,
            "place_id": "nonexistent-id"
        }
        resp = self.client.post(f"/api/v1/reviews/", json=review_payload)
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_create_review_empty_text(self):
        # First, create a place
        place_payload = {
            "title": "Tiny Home",
            "description": "Small but nice",
            "price": 80.0,
            "latitude": 30.0,
            "longitude": -100.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_resp = self.client.post("/api/v1/places/", json=place_payload)
        place_id = place_resp.get_json()["id"]

        review_payload = {
            "text": "",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": place_id
        }
        resp = self.client.post(f"/api/v1/reviews/", json=review_payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_create_review_invalid_user(self):
        # First, create a place
        place_payload = {
            "title": "Lake House",
            "description": "Near lake",
            "price": 150.0,
            "latitude": 42.0,
            "longitude": -88.0,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_resp = self.client.post("/api/v1/places/", json=place_payload)
        place_id = place_resp.get_json()["id"]

        review_payload = {
            "text": "Nice view",
            "rating": 4,
            "user_id": "nonexistent-user",
            "place_id": place_id
        }
        resp = self.client.post(f"/api/v1/reviews/", json=review_payload)
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn("error", data)

    # -------------------------
    # Other tests
    # -------------------------
    def test_delete_nonexistent_place(self):
        resp = self.client.delete("/api/v1/places/nonexistent-id")
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_get_nonexistent_user(self):
        resp = self.client.get("/api/v1/users/nonexistent-id")
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
