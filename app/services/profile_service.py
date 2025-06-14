"""
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
