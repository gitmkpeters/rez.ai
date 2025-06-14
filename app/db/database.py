"""
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
