#!/usr/bin/env python3
"""
Run Flask app on HTTP only - no SSL issues
"""

from app import create_app
import os

def main():
    """Run the Flask app on HTTP for development"""
    
    print("🚀 Resume Tailor - HTTP Development Server")
    print("=" * 50)
    print("📍 URL: http://localhost:5000")
    print("🔧 Mode: Development")
    print("🛡️  SSL: Disabled")
    print("📁 Output: ./output/ and ./app/output/")
    print("=" * 50)
    
    # Set environment variables to force HTTP
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Create the Flask app
    app = create_app()
    
    # Configure for HTTP development
    app.config.update(
        DEBUG=True,
        TESTING=False,
        PREFERRED_URL_SCHEME='http'
    )
    
    # Run on HTTP only
    try:
        print("🎯 Starting server...")
        app.run(
            host='127.0.0.1',  # localhost only
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True,
            ssl_context=None  # Explicitly no SSL
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
