from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

def admin_required():
    claims = get_jwt()
    return claims.get("is_admin", False)

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""

        user_id = get_jwt_identity()
        data = api.payload

        data["user_id"] = user_id

        place = facade.get_place(data["place_id"])

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id == user_id:
            return {"error": "You cannot review your own place"}, 400

        existing = facade.get_review_by_user_and_place(user_id, data["place_id"])

        if existing:
            return {"error": "You have already reviewed this place"}, 400

        try:
            review = facade.create_review(data)

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }, 201

        except ValueError:
            return {'error': 'Invalid input data'}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()

        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id,
                'place_id': r.place.id
            }
            for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200


    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        current_user = get_jwt_identity()

        if review.user.id != current_user and not admin_required():
            return {"error": "Unauthorized action"}, 403
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                return {'error': 'Review not found'}, 404

            return {'id': updated.id}, 200
        except ValueError:
            return {'error': 'Invalid input data'}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        current_user = get_jwt_identity()

        if review.user.id != current_user and not admin_required():
            return {"error": "Unauthorized action"}, 403
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200
