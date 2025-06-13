import os
from flask import Flask
import logging
from dotenv import load_dotenv

def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and configure the app
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'uploads'),
        OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
