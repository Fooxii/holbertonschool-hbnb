from flask import Flask
from flask_restx import Api
from config import config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended.exceptions import NoAuthorizationError

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]


    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"error": "Authorization header is missing"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"error": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"error": "Token has expired"}, 401

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    @api.errorhandler(NoAuthorizationError)
    def handle_auth_error(error):
        return {"error": "Authorization header is missing"}, 401

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
