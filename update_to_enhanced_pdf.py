"""
Update the services to use the enhanced PDF service with placeholder removal
"""
import os
import shutil

def update_pdf_service():
    """Replace the current PDF service with the enhanced version"""
    
    # Backup current PDF service
    current_pdf = "app/services/pdf_service.py"
    backup_pdf = "app/services/pdf_service.py.backup2"
    
    if os.path.exists(current_pdf):
        shutil.copy(current_pdf, backup_pdf)
        print(f"✅ Backed up {current_pdf} to {backup_pdf}")
    
    # Copy enhanced PDF service
    enhanced_pdf = "app/services/enhanced_pdf_service.py"
    if os.path.exists(enhanced_pdf):
        # Read the enhanced service and update class name
        with open(enhanced_pdf, 'r') as f:
            content = f.read()
        
        # Replace class name
        content = content.replace("class EnhancedPDFService:", "class PDFService:")
        
        # Write to pdf_service.py
        with open(current_pdf, 'w') as f:
            f.write(content)
        
        print("✅ Updated pdf_service.py with enhanced formatting")
        print("\nImprovements added:")
        print("- Placeholder text removal ([Your Name], [Company Name], etc.)")
        print("- Better bullet point handling (skips empty bullets)")
        print("- Improved section detection")
        print("- Enhanced content organization")
        
        return True
    else:
        print("❌ enhanced_pdf_service.py not found")
        return False

def test_enhanced_service():
    """Test the enhanced PDF service"""
    print("\n=== Testing Enhanced PDF Service ===")
    
    try:
        from app.services.pdf_service import PDFService
        pdf_service = PDFService()
        
        # Test with content containing placeholders
        test_content = """Mike Peterson
Denver, CO
mike@jprflipside.com
720-544-1525

PROFESSIONAL SUMMARY
[Your Name]
Dedicated dream builder with a passion for creating dreams and turning them into reality. Strong background in envisioning and executing projects that bring visions to life.

WORK EXPERIENCE
•
Dream Builder
[Company Name], [Location] [Dates]
• Spearheaded and executed dream projects from concept to completion, ensuring every detail aligned with the vision.
• Collaborated with teams to bring dreams to reality by overseeing timelines, budgets, and resources effectively.

EDUCATION
School of Dreams on the Cloud U [Degree Earned]
[Graduation Year]

SKILLS
• California Dreamin
• Visionary Thinking
• Project Management
• Team Collaboration
• Creative Problem Solving

OTHER
[Your Address]
[City, State, Zip Code] [Email Address] [Phone Number]
"""
        
        result = pdf_service.generate_resume_pdf(test_content, "Mike_Peterson_Enhanced")
        print(f"Test result: {result}")
        
        if result["success"]:
            print(f"✅ Enhanced PDF created: {result['filename']}")
            print(f"File size: {result.get('file_size', 'Unknown')} bytes")
        else:
            print(f"❌ Test failed: {result['message']}")
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Updating to Enhanced PDF Service ===")
    
    if update_pdf_service():
        print("\n" + "="*50)
        print("Next steps:")
        print("1. Restart your Flask app")
        print("2. Generate a new resume")
        print("3. Check the enhanced PDF formatting")
        
        # Test the enhanced service
        test_enhanced_service()
    else:
        print("Update failed - manual intervention required")