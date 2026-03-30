from app import create_app, db

app = create_app()

with app.app_context():
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity

    db.create_all()
    print("Tables created!")
