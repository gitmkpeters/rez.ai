"""
Fix the cover letter PDF generation by using smart placeholder removal
"""
import os
import shutil

def update_pdf_service():
    """Replace the current PDF service with the smart version"""
    
    # Backup current PDF service
    current_pdf = "app/services/pdf_service.py"
    backup_pdf = "app/services/pdf_service.py.backup3"
    
    if os.path.exists(current_pdf):
        shutil.copy(current_pdf, backup_pdf)
        print(f"✅ Backed up {current_pdf} to {backup_pdf}")
    
    # Copy smart PDF service
    smart_pdf = "app/services/smart_pdf_service.py"
    if os.path.exists(smart_pdf):
        # Read the smart service and update class name
        with open(smart_pdf, 'r') as f:
            content = f.read()
        
        # Replace class name
        content = content.replace("class SmartPDFService:", "class PDFService:")
        
        # Write to pdf_service.py
        with open(current_pdf, 'w') as f:
            f.write(content)
        
        print("✅ Updated pdf_service.py with smart formatting")
        print("\nImprovements added:")
        print("- Smart placeholder removal (different for resumes vs cover letters)")
        print("- Preserves cover letter structure and content")
        print("- Removes only unfilled placeholders from resumes")
        print("- Cleans up trailing metadata and instructions")
        
        return True
    else:
        print("❌ smart_pdf_service.py not found")
        return False

def test_smart_service():
    """Test the smart PDF service"""
    print("\n=== Testing Smart PDF Service ===")
    
    try:
        from app.services.pdf_service import PDFService
        pdf_service = PDFService()
        
        # Test cover letter content
        test_cover_letter = """Mike Peterson
Denver, CO
mike@jprflipside.com
720-544-1525

December 12, 2025

Hiring Manager
Dream Company
123 Dream Street
Dream City, CA 90210

Dear Hiring Manager,

I am writing to express my interest in the Dream Builder position at Dream Company, as advertised. With a passion for creating dreams and a proven track record as a dream builder, I am excited about the opportunity to contribute to your team.

As a dream builder with a keen eye for detail and a knack for turning visions into reality, I am confident in my ability to excel in this role. My experience has honed my skills in California dreamin', allowing me to bring innovative ideas to the table and execute them effectively.

I am particularly drawn to Dream Company's vision in helping individuals create the life of their dreams, as it aligns perfectly with my own professional mission. I am excited about the prospect of utilizing my skills and expertise to contribute to your team.

Thank you for considering my application. I look forward to the possibility of discussing how my skills and experiences align with the needs of your team.

Warm regards,
Mike Peterson"""
        
        result = pdf_service.generate_cover_letter_pdf(test_cover_letter, "Mike_Peterson_CoverLetter")
        print(f"Cover letter test result: {result}")
        
        if result["success"]:
            print(f"✅ Smart cover letter PDF created: {result['filename']}")
            print(f"File size: {result.get('file_size', 'Unknown')} bytes")
        else:
            print(f"❌ Test failed: {result['message']}")
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Fixing Cover Letter PDF Generation ===")
    
    if update_pdf_service():
        print("\n" + "="*50)
        print("Next steps:")
        print("1. Restart your Flask app")
        print("2. Generate a new cover letter")
        print("3. Check the improved cover letter PDF formatting")
        
        # Test the smart service
        test_smart_service()
    else:
        print("Update failed - manual intervention required")
