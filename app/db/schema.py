"""
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
