import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("=== Service Initialization Debug ===")

# Test each service individually
print("\n1. Testing JobScraper...")
try:
    from app.services.scraper import JobScraper
    scraper = JobScraper()
    print("✅ JobScraper initialized successfully")
except Exception as e:
    print(f"❌ JobScraper failed: {str(e)}")
    scraper = None

print("\n2. Testing DocumentService...")
try:
    from app.services.document_service import DocumentService
    document_service = DocumentService()
    print("✅ DocumentService initialized successfully")
except Exception as e:
    print(f"❌ DocumentService failed: {str(e)}")
    document_service = None

print("\n3. Testing OpenAIService...")
try:
    from app.services.openai_service import OpenAIService
    openai_service = OpenAIService()
    print("✅ OpenAIService initialized successfully")
except Exception as e:
    print(f"❌ OpenAIService failed: {str(e)}")
    openai_service = None

print("\n4. Testing SimplePDFService...")
try:
    from app.services.simple_pdf_service import SimplePDFService
    pdf_service = SimplePDFService()
    print("✅ SimplePDFService initialized successfully")
except Exception as e:
    print(f"❌ SimplePDFService failed: {str(e)}")
    pdf_service = None

print("\n5. Testing ResumeService...")
try:
    from app.services.resume_service import ResumeService
    resume_service = ResumeService(scraper, document_service, openai_service, pdf_service)
    print("✅ ResumeService initialized successfully")
    print(f"ResumeService methods: {[method for method in dir(resume_service) if not method.startswith('_')]}")
except Exception as e:
    print(f"❌ ResumeService failed: {str(e)}")
    import traceback
    traceback.print_exc()
    resume_service = None

print("\n6. Testing services import...")
try:
    from app.services import resume_service as imported_resume_service
    if imported_resume_service is None:
        print("❌ Imported resume_service is None")
    else:
        print("✅ resume_service imported successfully")
        print(f"Has generate_tailored_resume: {hasattr(imported_resume_service, 'generate_tailored_resume')}")
except Exception as e:
    print(f"❌ Services import failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== Environment Check ===")
print(f"OPENAI_API_KEY set: {'OPENAI_API_KEY' in os.environ}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
