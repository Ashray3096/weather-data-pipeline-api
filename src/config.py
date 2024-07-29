import os

class Config:
    # Database URI configuration for SQLAlchemy.
    # Retrieves the database URL from the environment variable 'DATABASE_URL'.
    # If 'DATABASE_URL' is not set, it defaults to a PostgreSQL database with the URI:
    # 'postgresql://postgres:root@localhost/cropyielddb'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/cropyielddb')

    # Disables the modification tracking feature of SQLAlchemy.
    # This setting is recommended for performance reasons and to avoid unnecessary overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False