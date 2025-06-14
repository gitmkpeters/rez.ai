"""
User Profile Repository

This module provides data access methods for user profiles and related entities.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.db.database import Database
from app.models.user_profile import UserProfile, WorkExperience, Education, Certification, Skill

logger = logging.getLogger(__name__)

class UserProfileRepository:
    """Repository for user profile data access"""
    
    def __init__(self):
        self.db = Database()
    
    def create_profile(self, profile: UserProfile) -> Optional[int]:
        """Create a new user profile"""
        query = """
        INSERT INTO user_profiles (user_id, full_name, email, phone, location, linkedin, website, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            profile.user_id,
            profile.full_name,
            profile.email,
            profile.phone,
            profile.location,
            profile.linkedin,
            profile.website,
            profile.summary
        )
        
        cursor = self.db.execute(query, params)
        if cursor:
            profile_id = cursor.lastrowid
            logger.info(f"Created user profile with ID: {profile_id}")
            
            # Save related entities
            if profile.work_experiences:
                for exp in profile.work_experiences:
                    exp.profile_id = profile_id
                    self.add_work_experience(exp)
            
            if profile.education:
                for edu in profile.education:
                    edu.profile_id = profile_id
                    self.add_education(edu)
            
            if profile.certifications:
                for cert in profile.certifications:
                    cert.profile_id = profile_id
                    self.add_certification(cert)
            
            if profile.skills:
                for skill in profile.skills:
                    skill.profile_id = profile_id
                    self.add_skill(skill)
            
            return profile_id
        return None
    
    def update_profile(self, profile: UserProfile) -> bool:
        """Update an existing user profile"""
        query = """
        UPDATE user_profiles
        SET full_name = ?, email = ?, phone = ?, location = ?, linkedin = ?, website = ?, summary = ?
        WHERE id = ?
        """
        params = (
            profile.full_name,
            profile.email,
            profile.phone,
            profile.location,
            profile.linkedin,
            profile.website,
            profile.summary,
            profile.id
        )
        
        cursor = self.db.execute(query, params)
        if cursor and cursor.rowcount > 0:
            logger.info(f"Updated user profile with ID: {profile.id}")
            return True
        return False
    
    def get_profile_by_id(self, profile_id: int) -> Optional[UserProfile]:
        """Get a user profile by ID with all related entities"""
        query = "SELECT * FROM user_profiles WHERE id = ?"
        row = self.db.fetch_one(query, (profile_id,))
        
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
            
            # Load related entities
            profile.work_experiences = self.get_work_experiences_by_profile_id(profile_id)
            profile.education = self.get_education_by_profile_id(profile_id)
            profile.certifications = self.get_certifications_by_profile_id(profile_id)
            profile.skills = self.get_skills_by_profile_id(profile_id)
            
            return profile
        return None
    
    def get_profile_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        """Get a user profile by user_id with all related entities"""
        query = "SELECT * FROM user_profiles WHERE user_id = ?"
        row = self.db.fetch_one(query, (user_id,))
        
        if row:
            profile_id = row['id']
            profile = UserProfile(
                id=profile_id,
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
            
            # Load related entities
            profile.work_experiences = self.get_work_experiences_by_profile_id(profile_id)
            profile.education = self.get_education_by_profile_id(profile_id)
            profile.certifications = self.get_certifications_by_profile_id(profile_id)
            profile.skills = self.get_skills_by_profile_id(profile_id)
            
            return profile
        return None
    
    def delete_profile(self, profile_id: int) -> bool:
        """Delete a user profile and all related entities"""
        query = "DELETE FROM user_profiles WHERE id = ?"
        cursor = self.db.execute(query, (profile_id,))
        if cursor and cursor.rowcount > 0:
            logger.info(f"Deleted user profile with ID: {profile_id}")
            return True
        return False
    
    def get_all_profiles(self) -> List[UserProfile]:
        """Get all user profiles (without related entities for performance)"""
        query = "SELECT * FROM user_profiles ORDER BY updated_at DESC"
        rows = self.db.fetch_all(query)
        
        profiles = []
        for row in rows:
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
            profiles.append(profile)
        
        return profiles
    
    # Work Experience methods
    def add_work_experience(self, experience: WorkExperience) -> Optional[int]:
        """Add a work experience to a profile"""
        query = """
        INSERT INTO work_experiences (profile_id, company, position, start_date, end_date, is_current, description, achievements)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            experience.profile_id,
            experience.company,
            experience.position,
            experience.start_date,
            experience.end_date,
            1 if experience.is_current else 0,
            experience.description,
            experience.achievements
        )
        
        cursor = self.db.execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None
    
    def update_work_experience(self, experience: WorkExperience) -> bool:
        """Update a work experience"""
        query = """
        UPDATE work_experiences
        SET company = ?, position = ?, start_date = ?, end_date = ?, is_current = ?, description = ?, achievements = ?
        WHERE id = ?
        """
        params = (
            experience.company,
            experience.position,
            experience.start_date,
            experience.end_date,
            1 if experience.is_current else 0,
            experience.description,
            experience.achievements,
            experience.id
        )
        
        cursor = self.db.execute(query, params)
        return cursor is not None and cursor.rowcount > 0
    
    def delete_work_experience(self, experience_id: int) -> bool:
        """Delete a work experience"""
        query = "DELETE FROM work_experiences WHERE id = ?"
        cursor = self.db.execute(query, (experience_id,))
        return cursor is not None and cursor.rowcount > 0
    
    def get_work_experiences_by_profile_id(self, profile_id: int) -> List[WorkExperience]:
        """Get all work experiences for a profile"""
        query = "SELECT * FROM work_experiences WHERE profile_id = ? ORDER BY is_current DESC, start_date DESC"
        rows = self.db.fetch_all(query, (profile_id,))
        
        experiences = []
        for row in rows:
            experience = WorkExperience(
                id=row['id'],
                profile_id=row['profile_id'],
                company=row['company'],
                position=row['position'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                is_current=bool(row['is_current']),
                description=row['description'],
                achievements=row['achievements'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            experiences.append(experience)
        
        return experiences
    
    # Education methods
    def add_education(self, education: Education) -> Optional[int]:
        """Add education to a profile"""
        query = """
        INSERT INTO education (profile_id, institution, degree, field_of_study, start_date, end_date, is_current, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            education.profile_id,
            education.institution,
            education.degree,
            education.field_of_study,
            education.start_date,
            education.end_date,
            1 if education.is_current else 0,
            education.description
        )
        
        cursor = self.db.execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None
    
    def update_education(self, education: Education) -> bool:
        """Update education"""
        query = """
        UPDATE education
        SET institution = ?, degree = ?, field_of_study = ?, start_date = ?, end_date = ?, is_current = ?, description = ?
        WHERE id = ?
        """
        params = (
            education.institution,
            education.degree,
            education.field_of_study,
            education.start_date,
            education.end_date,
            1 if education.is_current else 0,
            education.description,
            education.id
        )
        
        cursor = self.db.execute(query, params)
        return cursor is not None and cursor.rowcount > 0
    
    def delete_education(self, education_id: int) -> bool:
        """Delete education"""
        query = "DELETE FROM education WHERE id = ?"
        cursor = self.db.execute(query, (education_id,))
        return cursor is not None and cursor.rowcount > 0
    
    def get_education_by_profile_id(self, profile_id: int) -> List[Education]:
        """Get all education for a profile"""
        query = "SELECT * FROM education WHERE profile_id = ? ORDER BY is_current DESC, end_date DESC"
        rows = self.db.fetch_all(query, (profile_id,))
        
        education_list = []
        for row in rows:
            education = Education(
                id=row['id'],
                profile_id=row['profile_id'],
                institution=row['institution'],
                degree=row['degree'],
                field_of_study=row['field_of_study'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                is_current=bool(row['is_current']),
                description=row['description'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            education_list.append(education)
        
        return education_list
    
    # Certification methods
    def add_certification(self, certification: Certification) -> Optional[int]:
        """Add certification to a profile"""
        query = """
        INSERT INTO certifications (profile_id, name, issuing_organization, issue_date, expiration_date, credential_id, credential_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            certification.profile_id,
            certification.name,
            certification.issuing_organization,
            certification.issue_date,
            certification.expiration_date,
            certification.credential_id,
            certification.credential_url
        )
        
        cursor = self.db.execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None
    
    def update_certification(self, certification: Certification) -> bool:
        """Update certification"""
        query = """
        UPDATE certifications
        SET name = ?, issuing_organization = ?, issue_date = ?, expiration_date = ?, credential_id = ?, credential_url = ?
        WHERE id = ?
        """
        params = (
            certification.name,
            certification.issuing_organization,
            certification.issue_date,
            certification.expiration_date,
            certification.credential_id,
            certification.credential_url,
            certification.id
        )
        
        cursor = self.db.execute(query, params)
        return cursor is not None and cursor.rowcount > 0
    
    def delete_certification(self, certification_id: int) -> bool:
        """Delete certification"""
        query = "DELETE FROM certifications WHERE id = ?"
        cursor = self.db.execute(query, (certification_id,))
        return cursor is not None and cursor.rowcount > 0
    
    def get_certifications_by_profile_id(self, profile_id: int) -> List[Certification]:
        """Get all certifications for a profile"""
        query = "SELECT * FROM certifications WHERE profile_id = ? ORDER BY issue_date DESC"
        rows = self.db.fetch_all(query, (profile_id,))
        
        certifications = []
        for row in rows:
            certification = Certification(
                id=row['id'],
                profile_id=row['profile_id'],
                name=row['name'],
                issuing_organization=row['issuing_organization'],
                issue_date=row['issue_date'],
                expiration_date=row['expiration_date'],
                credential_id=row['credential_id'],
                credential_url=row['credential_url'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            certifications.append(certification)
        
        return certifications
    
    # Skill methods
    def add_skill(self, skill: Skill) -> Optional[int]:
        """Add skill to a profile"""
        query = """
        INSERT INTO skills (profile_id, name, level, category)
        VALUES (?, ?, ?, ?)
        """
        params = (
            skill.profile_id,
            skill.name,
            skill.level,
            skill.category
        )
        
        cursor = self.db.execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None
    
    def update_skill(self, skill: Skill) -> bool:
        """Update skill"""
        query = """
        UPDATE skills
        SET name = ?, level = ?, category = ?
        WHERE id = ?
        """
        params = (
            skill.name,
            skill.level,
            skill.category,
            skill.id
        )
        
        cursor = self.db.execute(query, params)
        return cursor is not None and cursor.rowcount > 0
    
    def delete_skill(self, skill_id: int) -> bool:
        """Delete skill"""
        query = "DELETE FROM skills WHERE id = ?"
        cursor = self.db.execute(query, (skill_id,))
        return cursor is not None and cursor.rowcount > 0
    
    def get_skills_by_profile_id(self, profile_id: int) -> List[Skill]:
        """Get all skills for a profile"""
        query = "SELECT * FROM skills WHERE profile_id = ? ORDER BY category, name"
        rows = self.db.fetch_all(query, (profile_id,))
        
        skills = []
        for row in rows:
            skill = Skill(
                id=row['id'],
                profile_id=row['profile_id'],
                name=row['name'],
                level=row['level'],
                category=row['category'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            skills.append(skill)
        
        return skills
