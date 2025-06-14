"""
Database Initialization Script

Run this script to initialize the SQLite database with the required schema.
"""

import logging
from app.db.schema import initialize_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Initialize the database"""
    print("🚀 Initializing Resume Tailor Database...")
    print("=" * 50)
    
    try:
        success = initialize_database()
        
        if success:
            print("✅ Database initialized successfully!")
            print("\nDatabase features:")
            print("- User profiles with contact information")
            print("- Work experience tracking")
            print("- Education history")
            print("- Skills and expertise levels")
            print("- Certifications and credentials")
            print("- Automatic timestamps and data integrity")
            print("\nYou can now:")
            print("1. Start the Flask application")
            print("2. Visit /profile to create your profile")
            print("3. Generate tailored resumes using your saved data")
        else:
            print("❌ Failed to initialize database")
            print("Check the logs for error details")
    
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")

if __name__ == "__main__":
    main()
