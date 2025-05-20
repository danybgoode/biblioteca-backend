from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    abs_user_id = db.Column(db.String(100))  # Stores Audiobookshelf user ID
    plan = db.Column(db.String(20), nullable=False)  # New: store plan