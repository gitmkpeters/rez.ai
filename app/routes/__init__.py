from flask import Blueprint

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes after Blueprint creation to avoid circular imports
from .main import main_bp