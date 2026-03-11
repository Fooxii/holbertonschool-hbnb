from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

def admin_required():
    claims = get_jwt()
    return claims.get("is_admin", False)

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403
        try:
            place = facade.create_place(api.payload)
            return {'id': place.id}, 201
        except (ValueError, TypeError):
            return {'error': 'Invalid input data'}, 400


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        return [
            {
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'latitude': p.latitude,
                'longitude': p.longitude
            }
            for p in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {'id': a.id, 'name': a.name}
                for a in place.amenities
            ]
        }, 200


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403
        try:
            updated = facade.update_place(place_id, api.payload)
            if not updated:
                return {'error': 'Place not found'}, 404

            return {'id': updated.id}, 200
        except ValueError:
            return {'error': 'Invalid input data'}, 400


    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403
        deleted = facade.delete_place(place_id)
        if not deleted:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place deleted successfully'}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)

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
