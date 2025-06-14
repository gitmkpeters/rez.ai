"""
Database Connection Manager

This module handles SQLite database connections and initialization with proper threading support.
"""

import os
import sqlite3
import logging
import threading
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    """SQLite database connection manager with thread-safe connections"""
    
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'app', 'data', 'resume_tailor.db')
        self.ensure_db_directory()
        # Use thread-local storage for connections
        self._local = threading.local()
    
    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Database directory ensured: {db_dir}")
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a thread-safe database connection"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            try:
                self._local.connection = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,  # Allow connection sharing
                    timeout=30.0  # 30 second timeout
                )
                self._local.connection.row_factory = sqlite3.Row
                # Enable WAL mode for better concurrency
                self._local.connection.execute('PRAGMA journal_mode=WAL')
                self._local.connection.execute('PRAGMA synchronous=NORMAL')
                self._local.connection.execute('PRAGMA cache_size=1000')
                self._local.connection.execute('PRAGMA temp_store=memory')
                logger.info(f"Connected to database: {self.db_path}")
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {str(e)}")
                raise
        return self._local.connection
    
    def close(self):
        """Close the thread-local database connection"""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None
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
