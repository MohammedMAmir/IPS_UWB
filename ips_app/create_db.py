from server import app, db

# Run this script to make an instance of the database
with app.app_context():
    db.create_all()