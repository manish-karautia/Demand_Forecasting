# ci/create_users_db.py

# This script initializes users.db during CI tests.
# It does NOT affect your production or local database.

from app import create_app, db
from app.db import User

app = create_app()

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="test@example.com").first():
        u = User(email="test@example.com", password="hashed_password")
        db.session.add(u)
        db.session.commit()

print("✓ SQLite users.db created for CI with test user.")
