from flask import Flask
from .extensions import db, create_minio_client
from .config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    """
    Application factory function for creating and configuring the Flask application.

    Args:
        config_class (class): The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register error handlers
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Create database tables and initialize MinIO client
    with app.app_context():
        db.create_all()
        app.minio_client = create_minio_client(app)

    return app