# app/services/resume_service.py

import os
import logging
from app.services.scraper import JobScraper
from app.services.openai_service import OpenAIService
from app.services.document_service import DocumentService
from werkzeug.utils import secure_filename

class ResumeService:
    def __init__(self):
        self.scraper = JobScraper()
        self.openai_service = OpenAIService()
        self.document_service = DocumentService()
        self.logger = logging.getLogger(__name__)
    
    def process_resume(self, resume_file, job_description=None, job_url=None):
        """Process resume with job description or URL"""
        try:
            # Extract text from resume
            resume_filename = secure_filename(resume_file.filename)
            resume_text = self.document_service.extract_text_from_file(resume_file)
            
            # Get job description from URL if provided
            if job_url and not job_description:
                try:
                    self.logger.info(f"Extracting job description from URL: {job_url}")
                    job_description = self.scraper.extract_job_description(job_url)
                except Exception as e:
                    self.logger.error(f"Error extracting job description from URL: {str(e)}")
                    raise ValueError(f"Failed to extract job description from URL: {str(e)}")
            
            if not job_description:
                raise ValueError("Job description is required")
            
            # Generate tailored resume using OpenAI
            tailored_resume = self.openai_service.tailor_resume(resume_text, job_description)
            
            # Generate PDF
            output_filename = f"tailored_{os.path.splitext(resume_filename)[0]}.pdf"
            pdf_path = self.document_service.generate_pdf(tailored_resume, output_filename)
            
            return {
                'pdf_path': pdf_path,
                'filename': output_filename
            }
            
        except Exception as e:
            self.logger.error(f"Error processing resume: {str(e)}")
            raise