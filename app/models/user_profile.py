"""
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
