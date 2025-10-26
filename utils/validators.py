"""
Pydantic schemas for data validation
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field, validator


class WorkHistory(BaseModel):
    """Work experience entry"""
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    dates: str = Field(..., description="Format: YYYY-MM to YYYY-MM or 'Present'")
    bullets: List[str] = Field(default_factory=list, max_items=10)

    @validator('bullets')
    def validate_bullets(cls, v):
        return [bullet.strip() for bullet in v if bullet.strip()]


class Education(BaseModel):
    """Education entry"""
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    year: str = Field(..., description="Graduation year or date range")
    gpa: Optional[str] = None
    honors: Optional[List[str]] = None


class Project(BaseModel):
    """Project entry"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    technologies: List[str] = Field(default_factory=list, max_items=20)
    link: Optional[str] = None
    github_url: Optional[str] = None

    @validator('link', 'github_url')
    def validate_url(cls, v):
        if v and not (v.startswith('http://') or v.startswith('https://')):
            return f'https://{v}'
        return v


class ContactInfo(BaseModel):
    """Contact information"""
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None


class ProfileSchema(BaseModel):
    """Complete profile schema for parsed resume data"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    linkedin_url: Optional[str] = None
    work_history: List[WorkHistory] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list, max_items=50)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    contact_info: Optional[ContactInfo] = None

    @validator('skills')
    def validate_skills(cls, v):
        # Remove duplicates and clean
        return list(set(skill.strip() for skill in v if skill.strip()))

    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Remove common formatting
            return v.strip()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maya Chen",
                "email": "maya.chen@example.com",
                "phone": "+1-555-123-4567",
                "linkedin_url": "https://linkedin.com/in/mayachen",
                "work_history": [
                    {
                        "title": "Frontend Developer Intern",
                        "company": "TechStartup Inc.",
                        "dates": "2023-06 to 2023-12",
                        "bullets": [
                            "Built React components for dashboard",
                            "Improved page load time by 40%"
                        ]
                    }
                ],
                "skills": ["React", "JavaScript", "Python"],
                "education": [
                    {
                        "degree": "Certificate in Web Development",
                        "institution": "General Assembly",
                        "year": "2023"
                    }
                ],
                "projects": [
                    {
                        "name": "Weather App",
                        "description": "Real-time weather dashboard",
                        "technologies": ["React", "Node.js"],
                        "link": "https://github.com/user/weather-app"
                    }
                ]
            }
        }


class OptimizerResult(BaseModel):
    """Result from resume optimizer"""
    score: int = Field(..., ge=0, le=100)
    missing_keywords: List[str] = Field(default_factory=list)
    suggestions: List[dict] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "score": 67,
                "missing_keywords": ["TypeScript", "RESTful APIs"],
                "suggestions": [
                    {
                        "section": "Skills",
                        "recommendation": "Add 'TypeScript' to demonstrate full-stack capability"
                    }
                ]
            }
        }


class MockInterviewQuestion(BaseModel):
    """Mock interview question"""
    type: str = Field(..., pattern="^(technical|behavioral)$")
    question: str = Field(..., min_length=10)


class MockInterviewFeedback(BaseModel):
    """Feedback for mock interview answer"""
    confidence_score: float = Field(..., ge=0, le=5)
    clarity: int = Field(..., ge=1, le=5)
    specificity: int = Field(..., ge=1, le=5)
    relevance: int = Field(..., ge=1, le=5)
    feedback: List[str] = Field(default_factory=list)


class CoverLetterRequest(BaseModel):
    """Request for cover letter generation"""
    job_description: str = Field(..., min_length=50, max_length=5000)
    tone: str = Field(..., pattern="^(formal|friendly|technical)$")
    company_name: Optional[str] = None


class JobAlertPreferences(BaseModel):
    """User preferences for job alerts"""
    keywords: List[str] = Field(..., min_items=1, max_items=20)
    sources: List[str] = Field(..., min_items=1)
    frequency: str = Field(..., pattern="^(daily|weekly)$")

    @validator('sources')
    def validate_sources(cls, v):
        valid_sources = ['linkedin', 'wellfound', 'angellist', 'indeed']
        return [s for s in v if s.lower() in valid_sources]

    @validator('keywords')
    def validate_keywords(cls, v):
        return [kw.strip() for kw in v if kw.strip()]


# File upload validation
class FileUploadValidator:
    """Validate file uploads"""

    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def validate_file(file, filename: str) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded file
        Returns: (is_valid, error_message)
        """
        # Check file extension
        import os
        ext = os.path.splitext(filename)[1].lower()
        if ext not in FileUploadValidator.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(FileUploadValidator.ALLOWED_EXTENSIONS)}"

        # Check file size
        try:
            file.seek(0, 2)  # Seek to end
            size = file.tell()
            file.seek(0)  # Reset to beginning

            if size > FileUploadValidator.MAX_FILE_SIZE:
                return False, f"File too large. Maximum size: 5MB"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

        return True, None


# LinkedIn URL validation
class LinkedInValidator:
    """Validate LinkedIn URLs"""

    VALID_PATTERNS = [
        r'linkedin\.com/in/[a-zA-Z0-9-]+',
        r'linkedin\.com/pub/[a-zA-Z0-9-]+',
    ]

    @staticmethod
    def is_valid_linkedin_url(url: str) -> bool:
        """Check if URL is a valid LinkedIn profile URL"""
        import re
        if not url:
            return False

        # Ensure https
        if not url.startswith('http'):
            url = f'https://{url}'

        for pattern in LinkedInValidator.VALID_PATTERNS:
            if re.search(pattern, url):
                return True
        return False

    @staticmethod
    def normalize_linkedin_url(url: str) -> str:
        """Normalize LinkedIn URL to standard format"""
        if not url.startswith('http'):
            url = f'https://{url}'

        # Remove query parameters and fragments
        import re
        url = re.sub(r'\?.*$', '', url)
        url = re.sub(r'#.*$', '', url)

        return url.rstrip('/')
