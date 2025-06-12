import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services with error handling
scraper = None
document_service = None
openai_service = None
pdf_service = None
resume_service = None

logger.info("Starting service initialization...")

# 1. Initialize JobScraper
try:
    from app.services.scraper import JobScraper
    scraper = JobScraper()
    logger.info("✅ JobScraper initialized")
except Exception as e:
    logger.error(f"❌ JobScraper failed: {str(e)}")

# 2. Initialize DocumentService
try:
    from app.services.document_service import DocumentService
    document_service = DocumentService()
    logger.info("✅ DocumentService initialized")
except Exception as e:
    logger.error(f"❌ DocumentService failed: {str(e)}")

# 3. Initialize OpenAIService
try:
    from app.services.openai_service import OpenAIService
    openai_service = OpenAIService()
    logger.info("✅ OpenAIService initialized")
except Exception as e:
    logger.error(f"❌ OpenAIService failed: {str(e)}")

# 4. Initialize PDF Service (try ReportLab PDFService first, then fallback to SimplePDFService)
try:
    from app.services.pdf_service import PDFService
    pdf_service = PDFService()
    logger.info("✅ PDFService (ReportLab) initialized - will create actual PDF files")
except Exception as e:
    logger.warning(f"⚠️ PDFService (ReportLab) failed: {str(e)}")
    try:
        from app.services.simple_pdf_service import SimplePDFService
        pdf_service = SimplePDFService()
        logger.info("✅ SimplePDFService initialized as fallback - will create text files")
    except Exception as e2:
        logger.error(f"❌ SimplePDFService also failed: {str(e2)}")

# 5. Initialize ResumeService (this is the critical one)
try:
    from app.services.resume_service import ResumeService
    
    # Initialize with exactly 4 arguments as expected
    resume_service = ResumeService(
        scraper=scraper,
        document_service=document_service, 
        openai_service=openai_service,
        pdf_service=pdf_service
    )
    logger.info("✅ ResumeService initialized")
    
    # Log which PDF service is being used
    if pdf_service:
        pdf_service_type = type(pdf_service).__name__
        logger.info(f"📄 PDF Service type: {pdf_service_type}")
        if pdf_service_type == "PDFService":
            logger.info("🎯 Using ReportLab PDFService - will generate actual PDF files")
        else:
            logger.info("📝 Using SimplePDFService - will generate text files")
    
    # Verify it has the required methods
    required_methods = ['generate_tailored_resume', 'generate_cover_letter', 'process_resume']
    for method in required_methods:
        if hasattr(resume_service, method):
            logger.info(f"✅ ResumeService has {method}")
        else:
            logger.error(f"❌ ResumeService missing {method}")
            
except Exception as e:
    logger.error(f"❌ ResumeService failed: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())
    
    # Use fallback service
    try:
        from app.services.fallback_resume_service import FallbackResumeService
        resume_service = FallbackResumeService()
        logger.warning("Using fallback resume service")
    except Exception as e2:
        logger.error(f"❌ Even fallback service failed: {str(e2)}")

# Log final status
services_status = {
    'scraper': scraper is not None,
    'document_service': document_service is not None,
    'openai_service': openai_service is not None,
    'pdf_service': pdf_service is not None,
    'resume_service': resume_service is not None
}

logger.info(f"Services initialized: {services_status}")

if resume_service is None:
    logger.error("CRITICAL: resume_service is None - the application will not work properly")
else:
    logger.info("SUCCESS: resume_service is available")
    if pdf_service:
        logger.info(f"PDF service ready: {type(pdf_service).__name__}")
