import logging
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=== Quick Service Debug ===")

try:
    print("Testing ResumeService constructor...")
    from app.services.scraper import JobScraper
    from app.services.document_service import DocumentService
    from app.services.openai_service import OpenAIService
    from app.services.simple_pdf_service import SimplePDFService
    from app.services.resume_service import ResumeService
    
    # Create individual services
    scraper = JobScraper()
    document_service = DocumentService()
    openai_service = OpenAIService()
    pdf_service = SimplePDFService()
    
    print("All individual services created successfully")
    
    # Test ResumeService constructor
    resume_service = ResumeService(
        scraper=scraper,
        document_service=document_service,
        openai_service=openai_service,
        pdf_service=pdf_service
    )
    
    print("✅ ResumeService created successfully!")
    print(f"ResumeService methods: {[m for m in dir(resume_service) if not m.startswith('_')]}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\nTesting services import...")
try:
    from app.services import resume_service
    if resume_service:
        print("✅ Services import successful!")
    else:
        print("❌ resume_service is None")
except Exception as e:
    print(f"❌ Services import failed: {str(e)}")
