import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("=== PDF Generation Debug ===")

# Test content
test_resume = """Mike Peterson
Denver, CO
mike@jprflipside.com
720-544-1525

Professional Summary:
Seasoned IT Specialist with 25 years of experience at the US Small Business Administration.

Work Experience:
Senior IT Specialist
U.S. Small Business Administration (SBA)
Denver, CO
Oct 2012 – Present

- Led team in managing financial reporting
- Developed SQL-based data pipelines
"""

print("1. Testing SimplePDFService...")
try:
    from app.services.simple_pdf_service import SimplePDFService
    pdf_service = SimplePDFService()
    
    result = pdf_service.generate_resume_pdf(test_resume, "Mike_Peterson")
    print(f"SimplePDFService result: {result}")
    
    if result["success"]:
        print(f"File path: {result['filepath']}")
        print(f"File exists: {os.path.exists(result['filepath'])}")
        if os.path.exists(result['filepath']):
            with open(result['filepath'], 'r') as f:
                content = f.read()
            print(f"File content length: {len(content)} characters")
    
except Exception as e:
    print(f"SimplePDFService failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n2. Testing ReportLab PDFService...")
try:
    from app.services.pdf_service import PDFService
    pdf_service = PDFService()
    
    result = pdf_service.generate_resume_pdf(test_resume, "Mike_Peterson")
    print(f"PDFService result: {result}")
    
    if result["success"]:
        print(f"File path: {result['filepath']}")
        print(f"File exists: {os.path.exists(result['filepath'])}")
        if os.path.exists(result['filepath']):
            file_size = os.path.getsize(result['filepath'])
            print(f"PDF file size: {file_size} bytes")
    
except Exception as e:
    print(f"PDFService failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n3. Checking output directories...")
possible_dirs = ["output", "app/output", "app/static/output", "."]
for directory in possible_dirs:
    exists = os.path.exists(directory)
    writable = False
    if exists:
        try:
            test_file = os.path.join(directory, "test_write.txt")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            writable = True
        except:
            pass
    print(f"Directory {directory}: exists={exists}, writable={writable}")

print("\n4. Testing ResumeService PDF generation...")
try:
    from app.services import resume_service
    
    if resume_service and hasattr(resume_service, 'pdf_service'):
        print(f"ResumeService has pdf_service: {resume_service.pdf_service is not None}")
        if resume_service.pdf_service:
            print(f"PDF service type: {type(resume_service.pdf_service)}")
            
            # Test direct PDF generation
            result = resume_service.pdf_service.generate_resume_pdf(test_resume, "Test_User")
            print(f"Direct PDF generation result: {result}")
    else:
        print("ResumeService or pdf_service not available")
        
except Exception as e:
    print(f"ResumeService PDF test failed: {str(e)}")
    import traceback
    traceback.print_exc()
