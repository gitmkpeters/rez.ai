"""
Update the services to use the improved PDF service
"""
import os
import shutil

def update_pdf_service():
    """Replace the current PDF service with the improved version"""
    
    # Backup current PDF service
    current_pdf = "app/services/pdf_service.py"
    backup_pdf = "app/services/pdf_service.py.backup"
    
    if os.path.exists(current_pdf):
        shutil.copy(current_pdf, backup_pdf)
        print(f"✅ Backed up {current_pdf} to {backup_pdf}")
    
    # Copy improved PDF service
    improved_pdf = "app/services/improved_pdf_service.py"
    if os.path.exists(improved_pdf):
        # Read the improved service and update class name
        with open(improved_pdf, 'r') as f:
            content = f.read()
        
        # Replace class name
        content = content.replace("class ImprovedPDFService:", "class PDFService:")
        
        # Write to pdf_service.py
        with open(current_pdf, 'w') as f:
            f.write(content)
        
        print("✅ Updated pdf_service.py with improved formatting")
        print("\nImprovements added:")
        print("- Better content parsing and section identification")
        print("- Proper bullet point formatting")
        print("- Enhanced typography and spacing")
        print("- Complete content preservation")
        print("- Professional styling")
        
        return True
    else:
        print("❌ improved_pdf_service.py not found")
        return False

def test_improved_service():
    """Test the improved PDF service"""
    print("\n=== Testing Improved PDF Service ===")
    
    try:
        from app.services.pdf_service import PDFService
        pdf_service = PDFService()
        
        # Test with more comprehensive content
        test_content = """Mike Peterson
Denver, CO
mike@jprflipside.com
720-544-1525
LinkedIn: linkedin.com/in/mikepeterson

Professional Summary
Seasoned IT Specialist with 25 years of experience at the US Small Business Administration, specializing in financial reporting systems, data pipeline development, and team leadership.

Work Experience

Senior IT Specialist
U.S. Small Business Administration (SBA)
Denver, CO
Oct 2012 – Present

- Led cross-functional team in managing comprehensive financial reporting systems
- Developed and maintained SQL-based data pipelines for critical business operations
- Implemented automated reporting solutions that reduced processing time by 40%
- Collaborated with stakeholders to identify and resolve system inefficiencies
- Mentored junior staff on best practices for data management and analysis

IT Analyst
U.S. Small Business Administration (SBA)
Denver, CO
Jan 2008 – Sep 2012

- Analyzed business requirements and translated them into technical specifications
- Maintained legacy systems while planning modernization initiatives
- Provided technical support for mission-critical applications

Education

Bachelor of Science in Information Technology
University of Colorado Denver
Graduated: 2007

Skills

Technical Skills:
- SQL Server, Oracle, MySQL
- Python, PowerShell, VBA
- Tableau, Power BI
- Windows Server, Linux
- Project Management

Soft Skills:
- Team Leadership
- Cross-functional Collaboration
- Problem Solving
- Communication
"""
        
        result = pdf_service.generate_resume_pdf(test_content, "Mike_Peterson_Improved")
        print(f"Test result: {result}")
        
        if result["success"]:
            print(f"✅ Improved PDF created: {result['filename']}")
            print(f"File size: {result.get('file_size', 'Unknown')} bytes")
        else:
            print(f"❌ Test failed: {result['message']}")
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Updating to Improved PDF Service ===")
    
    if update_pdf_service():
        print("\n" + "="*50)
        print("Next steps:")
        print("1. Restart your Flask app")
        print("2. Generate a new resume")
        print("3. Check the improved PDF formatting")
        
        # Test the improved service
        test_improved_service()
    else:
        print("Update failed - manual intervention required")
