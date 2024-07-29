from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db
from resources import api_bp

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    # Load configuration settings from Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    # Create and run the Flask application
    app = create_app()
    app.run(debug=True)
