from bookapi import app, db

with app.app_context():
    db.create_all()