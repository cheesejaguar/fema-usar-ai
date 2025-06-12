"""
Main Flask application entry point
"""
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from config import Config
from routes import register_routes
from services.vector_store import VectorStoreService
from services.llm_service import LLMService

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)

    # Rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

    # Initialize services
    vector_store = VectorStoreService()
    llm_service = LLMService(
        api_key=app.config.get("NEMO_API_KEY"),
        model=app.config.get("DEFAULT_MODEL"),
    )

    # Store services in app context
    app.vector_store = vector_store
    app.llm_service = llm_service
    app.limiter = limiter

    # Register routes
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
