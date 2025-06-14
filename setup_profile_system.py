#!/usr/bin/env python3
"""
Profile System Setup Script

This script creates all the necessary files for the complete profile management system.
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"✅ Created directory: {path}")
    else:
        logger.info(f"📁 Directory already exists: {path}")

def create_file(path, content):
    """Create file with content"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        logger.info(f"✅ Created file: {path}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create {path}: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Profile Management System")
    print("=" * 50)
    
    # Create directories
    directories = [
        'app/models',
        'app/db',
        'app/repositories',
        'app/data'  # For SQLite database
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Create __init__.py files
    init_files = [
        'app/models/__init__.py',
        'app/db/__init__.py',
        'app/repositories/__init__.py'
    ]
    
    for init_file in init_files:
        create_file(init_file, '# Package initialization\n')
    
    # Create user profile models
    models_content = '''"""
User Profile Models

This module defines the data models for user profiles and related entities.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class WorkExperience:
    id: Optional[int] = None
    profile_id: Optional[int] = None
    company: str = ""
    position: str = ""
    start_date: str = ""
    end_date: str = ""
    is_current: bool = False
    description: str = ""
    achievements: str = ""
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Education:
    id: Optional[int] = None
    profile_id: Optional[int] = None
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""
    is_current: bool = False
    description: str = ""
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Certification:
    id: Optional[int] = None
    profile_id: Optional[int] = None
    name: str = ""
    issuing_organization: str = ""
    issue_date: str = ""
    expiration_date: str = ""
    credential_id: str = ""
    credential_url: str = ""
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Skill:
    id: Optional[int] = None
    profile_id: Optional[int] = None
    name: str = ""
    level: str = ""  # e.g., "Beginner", "Intermediate", "Advanced", "Expert"
    category: str = ""  # e.g., "Technical", "Soft", "Language"
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class UserProfile:
    id: Optional[int] = None
    user_id: str = ""  # Could be email or username
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    website: str = ""
    summary: str = ""
    work_experiences: List[WorkExperience] = None
    education: List[Education] = None
    certifications: List[Certification] = None
    skills: List[Skill] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.work_experiences is None:
            self.work_experiences = []
        if self.education is None:
            self.education = []
        if self.certifications is None:
            self.certifications = []
        if self.skills is None:
            self.skills = []
'''
    
    create_file('app/models/user_profile.py', models_content)
    
    # Create database connection manager
    database_content = '''"""
Database Connection Manager

This module handles SQLite database connections and initialization.
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    """SQLite database connection manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.db_path = os.path.join(os.getcwd(), 'app', 'data', 'resume_tailor.db')
            self.ensure_db_directory()
            self.initialized = True
    
    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Database directory ensured: {db_dir}")
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection, creating one if needed"""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row
                logger.info(f"Connected to database: {self.db_path}")
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {str(e)}")
                raise
        return self.connection
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def execute_script(self, script: str) -> bool:
        """Execute a SQL script"""
        conn = self.get_connection()
        try:
            conn.executescript(script)
            conn.commit()
            logger.info("SQL script executed successfully")
            return True
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Error executing SQL script: {str(e)}")
            return False
    
    def execute(self, query: str, params=None) -> Optional[sqlite3.Cursor]:
        """Execute a SQL query with parameters"""
        conn = self.get_connection()
        try:
            if params:
                cursor = conn.execute(query, params)
            else:
                cursor = conn.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            return None
    
    def fetch_all(self, query: str, params=None) -> list:
        """Execute a query and fetch all results"""
        cursor = self.execute(query, params)
        if cursor:
            return cursor.fetchall()
        return []
    
    def fetch_one(self, query: str, params=None) -> Optional[sqlite3.Row]:
        """Execute a query and fetch one result"""
        cursor = self.execute(query, params)
        if cursor:
            return cursor.fetchone()
        return None
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(query, (table_name,))
        return result is not None
'''
    
    create_file('app/db/database.py', database_content)
    
    # Create database schema
    schema_content = '''"""
Database Schema

This module defines the database schema and provides functions to initialize the database.
"""

import logging
from app.db.database import Database

logger = logging.getLogger(__name__)

# SQL to create the user_profiles table
CREATE_USER_PROFILES_TABLE = """
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    linkedin TEXT,
    website TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# SQL to create the work_experiences table
CREATE_WORK_EXPERIENCES_TABLE = """
CREATE TABLE IF NOT EXISTS work_experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    is_current BOOLEAN DEFAULT 0,
    description TEXT,
    achievements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id) ON DELETE CASCADE
);
"""

# SQL to create the education table
CREATE_EDUCATION_TABLE = """
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field_of_study TEXT,
    start_date TEXT,
    end_date TEXT,
    is_current BOOLEAN DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id) ON DELETE CASCADE
);
"""

# SQL to create the certifications table
CREATE_CERTIFICATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    issuing_organization TEXT,
    issue_date TEXT,
    expiration_date TEXT,
    credential_id TEXT,
    credential_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id) ON DELETE CASCADE
);
"""

# SQL to create the skills table
CREATE_SKILLS_TABLE = """
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    level TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id) ON DELETE CASCADE
);
"""

def initialize_database():
    """Initialize the database with the required schema"""
    db = Database()
    
    # Create tables
    tables_created = True
    tables_created &= db.execute_script(CREATE_USER_PROFILES_TABLE)
    tables_created &= db.execute_script(CREATE_WORK_EXPERIENCES_TABLE)
    tables_created &= db.execute_script(CREATE_EDUCATION_TABLE)
    tables_created &= db.execute_script(CREATE_CERTIFICATIONS_TABLE)
    tables_created &= db.execute_script(CREATE_SKILLS_TABLE)
    
    if tables_created:
        logger.info("Database schema initialized successfully")
        return True
    else:
        logger.error("Failed to initialize database schema")
        return False
'''
    
    create_file('app/db/schema.py', schema_content)
    
    # Create a simple profile service
    service_content = '''"""
Profile Service

This module provides basic profile operations.
"""

import logging
from typing import Optional, Dict, Any
from app.models.user_profile import UserProfile
from app.db.database import Database

logger = logging.getLogger(__name__)

class ProfileService:
    """Service for user profile operations"""
    
    def __init__(self):
        self.db = Database()
    
    def get_profile_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        """Get a user profile by user_id"""
        try:
            query = "SELECT * FROM user_profiles WHERE user_id = ?"
            row = self.db.fetch_one(query, (user_id,))
            
            if row:
                profile = UserProfile(
                    id=row['id'],
                    user_id=row['user_id'],
                    full_name=row['full_name'],
                    email=row['email'],
                    phone=row['phone'],
                    location=row['location'],
                    linkedin=row['linkedin'],
                    website=row['website'],
                    summary=row['summary'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                return profile
            return None
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            return None
    
    def create_or_update_profile(self, profile_data: Dict[str, Any]) -> Optional[UserProfile]:
        """Create a new profile or update an existing one"""
        try:
            user_id = profile_data.get('user_id')
            if not user_id:
                logger.error("Cannot create profile without user_id")
                return None
            
            # Check if profile exists
            existing_profile = self.get_profile_by_user_id(user_id)
            
            if existing_profile:
                # Update existing profile
                query = """
                UPDATE user_profiles
                SET full_name = ?, email = ?, phone = ?, location = ?, linkedin = ?, website = ?, summary = ?
                WHERE user_id = ?
                """
                params = (
                    profile_data.get('full_name', ''),
                    profile_data.get('email', ''),
                    profile_data.get('phone', ''),
                    profile_data.get('location', ''),
                    profile_data.get('linkedin', ''),
                    profile_data.get('website', ''),
                    profile_data.get('summary', ''),
                    user_id
                )
                
                cursor = self.db.execute(query, params)
                if cursor and cursor.rowcount > 0:
                    logger.info(f"Updated profile for user: {user_id}")
                    return self.get_profile_by_user_id(user_id)
            else:
                # Create new profile
                query = """
                INSERT INTO user_profiles (user_id, full_name, email, phone, location, linkedin, website, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    user_id,
                    profile_data.get('full_name', ''),
                    profile_data.get('email', ''),
                    profile_data.get('phone', ''),
                    profile_data.get('location', ''),
                    profile_data.get('linkedin', ''),
                    profile_data.get('website', ''),
                    profile_data.get('summary', '')
                )
                
                cursor = self.db.execute(query, params)
                if cursor:
                    logger.info(f"Created profile for user: {user_id}")
                    return self.get_profile_by_user_id(user_id)
            
            return None
        except Exception as e:
            logger.error(f"Error creating/updating profile: {str(e)}")
            return None
    
    def add_work_experience(self, profile_id: int, experience_data: Dict[str, Any]) -> Optional[int]:
        """Add work experience to a profile"""
        try:
            query = """
            INSERT INTO work_experiences (profile_id, company, position, start_date, end_date, is_current, description, achievements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                profile_id,
                experience_data.get('company', ''),
                experience_data.get('position', ''),
                experience_data.get('start_date', ''),
                experience_data.get('end_date', ''),
                1 if experience_data.get('is_current', False) else 0,
                experience_data.get('description', ''),
                experience_data.get('achievements', '')
            )
            
            cursor = self.db.execute(query, params)
            if cursor:
                return cursor.lastrowid
            return None
        except Exception as e:
            logger.error(f"Error adding work experience: {str(e)}")
            return None
    
    def add_education(self, profile_id: int, education_data: Dict[str, Any]) -> Optional[int]:
        """Add education to a profile"""
        try:
            query = """
            INSERT INTO education (profile_id, institution, degree, field_of_study, start_date, end_date, is_current, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                profile_id,
                education_data.get('institution', ''),
                education_data.get('degree', ''),
                education_data.get('field_of_study', ''),
                education_data.get('start_date', ''),
                education_data.get('end_date', ''),
                1 if education_data.get('is_current', False) else 0,
                education_data.get('description', '')
            )
            
            cursor = self.db.execute(query, params)
            if cursor:
                return cursor.lastrowid
            return None
        except Exception as e:
            logger.error(f"Error adding education: {str(e)}")
            return None
    
    def add_skill(self, profile_id: int, skill_data: Dict[str, Any]) -> Optional[int]:
        """Add skill to a profile"""
        try:
            query = """
            INSERT INTO skills (profile_id, name, level, category)
            VALUES (?, ?, ?, ?)
            """
            params = (
                profile_id,
                skill_data.get('name', ''),
                skill_data.get('level', ''),
                skill_data.get('category', '')
            )
            
            cursor = self.db.execute(query, params)
            if cursor:
                return cursor.lastrowid
            return None
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            return None
    
    def delete_work_experience(self, experience_id: int) -> bool:
        """Delete work experience"""
        try:
            query = "DELETE FROM work_experiences WHERE id = ?"
            cursor = self.db.execute(query, (experience_id,))
            return cursor is not None and cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting work experience: {str(e)}")
            return False
    
    def delete_education(self, education_id: int) -> bool:
        """Delete education"""
        try:
            query = "DELETE FROM education WHERE id = ?"
            cursor = self.db.execute(query, (education_id,))
            return cursor is not None and cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting education: {str(e)}")
            return False
    
    def delete_skill(self, skill_id: int) -> bool:
        """Delete skill"""
        try:
            query = "DELETE FROM skills WHERE id = ?"
            cursor = self.db.execute(query, (skill_id,))
            return cursor is not None and cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting skill: {str(e)}")
            return False
'''
    
    create_file('app/services/profile_service.py', service_content)
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    try:
        from app.db.schema import initialize_database
        if initialize_database():
            print("✅ Database initialized successfully!")
        else:
            print("❌ Database initialization failed!")
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
    
    print("\n🎉 Profile system setup complete!")
    print("\nNext steps:")
    print("1. Restart your Flask app: python run.py")
    print("2. Visit: http://localhost:5000/profile")
    print("3. Test the profile management system")

if __name__ == "__main__":
    main()
