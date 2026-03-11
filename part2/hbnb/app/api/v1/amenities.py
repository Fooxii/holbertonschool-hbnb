from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def admin_required():
    """Check if current user is admin."""
    claims = get_jwt()
    return claims.get("is_admin", False)

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403
        try:
            amenity = facade.create_amenity(api.payload)
            return {'id': amenity.id}, 201
        except ValueError:
            return {'error': 'Invalid input data'}, 400


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {'id': a.id, 'name': a.name}
            for a in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'id': amenity.id, 'name': amenity.name}, 200


@api.expect(amenity_model)
@api.response(200, 'Amenity updated successfully')
@api.response(404, 'Amenity not found')
@api.response(400, 'Invalid input data')
@jwt_required()
def put(self, amenity_id):
    """Update an amenity's information"""
    if not admin_required():
        return {'error': 'Admin privileges required'}, 403
    try:
        updated = facade.update_amenity(amenity_id, api.payload)
        if not updated:
            return {'error': 'Amenity not found'}, 404

        return {'id': updated.id, 'name': updated.name}, 200
    except ValueError:
        return {'error': 'Invalid input data'}, 400
