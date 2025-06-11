from app.services.scraper import JobScraper
from app.services.document_service import DocumentService
from app.services.resume_service import ResumeService
from app.services.openai_service import OpenAIService

# Create instances of services
scraper = JobScraper()
document_service = DocumentService()
openai_service = OpenAIService()
resume_service = ResumeService(scraper, document_service, openai_service)