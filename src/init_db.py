# init_db.py

from app import create_app
from extensions import db

# Create and configure the Flask application
app = create_app()

# Establish an application context to allow database operations
with app.app_context():
    # Create all database tables defined in models
    db.create_all()
    print("Database tables created")
