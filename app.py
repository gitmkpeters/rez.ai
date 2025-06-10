import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Run the app if executed directly
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])