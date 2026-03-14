from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

def is_admin():
    claims = get_jwt()
    return claims.get("is_admin", False)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        print("Payload received:", user_data)
        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400
        print("New user object:", new_user)
        response = {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }
        print("Returning JSON:", response)
        return response, 201


    @api.response(200, 'List of users retrieved successfully')
    @jwt_required()
    def get(self):
        """Retrieve all users"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        current_user_id = get_jwt_identity()

        if current_user_id != user_id and not is_admin():
            return {'error': 'Unauthorized'}, 403

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'You cannot modify email or password')
    @jwt_required()
    def put(self, user_id):

        current_user = get_jwt_identity()

        if current_user != user_id and not is_admin():
            return {"error": "Unauthorized action"}, 403

        data = api.payload

        if not is_admin():
            if "email" in data or "password" in data:
                return {"error": "You cannot modify email or password"}, 400

        updated = facade.update_user(user_id, data)

        if not updated:
            return {"error": "User not found"}, 404

        return {"id": updated.id}, 200
