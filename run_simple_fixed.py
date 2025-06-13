#!/usr/bin/env python3
"""
Simple HTTP server for development (no SSL issues)
"""

from app import create_app
import os

def main():
    """Run the Flask app on HTTP for development"""
    
    print("🚀 Starting Resume Tailor - Development Server")
    print("=" * 50)
    print("📍 Running on: http://localhost:5000")
    print("🔧 Mode: Development (HTTP only)")
    print("🛡️  SSL: Disabled for local development")
    print("=" * 50)
    
    # Create the Flask app
    app = create_app()
    
    # Configure for development
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
    # Run without SSL
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
