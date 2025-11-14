from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


def init_db(app):
    with app.app_context():
        db.create_all()


def create_test_user(app):
    from app.database import User, db
    with app.app_context():
        if not User.query.filter_by(email="test@example.com").first():
            u = User(email="test@example.com", password="hashed_password")
            db.session.add(u)
            db.session.commit()
            print("✅ Test user created.")
