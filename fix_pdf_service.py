import os
import logging
from datetime import datetime
import re

class FixedPDFService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Create output directory if it doesn't exist
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_resume_pdf(self, resume_content, user_name="Resume"):
        """Generate a text file with proper formatting"""
        try:
            self.logger.info(f"Generating file for: {user_name}")
            
            # Create safe filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Resume_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            # Write content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("RESUME\n")
                f.write("=" * 50 + "\n\n")
                f.write(resume_content)
                f.write("\n\n" + "=" * 50)
                f.write(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            self.logger.info(f"File created: {filepath}")
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "message": f"Resume saved as: {filename}"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating file: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    def generate_cover_letter_pdf(self, cover_letter_content, user_name="Cover_Letter"):
        """Generate a cover letter text file"""
        try:
            # Create safe filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Cover_Letter_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            # Write content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("COVER LETTER\n")
                f.write("=" * 50 + "\n\n")
                f.write(cover_letter_content)
                f.write("\n\n" + "=" * 50)
                f.write(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "message": f"Cover letter saved as: {filename}"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter file: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

# Test the fixed service
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    service = FixedPDFService()
    
    test_content = """Mike Peterson
Denver, CO
mike@jprflipside.com

Professional Summary:
Seasoned IT Specialist with 25 years of experience.
"""
    
    result = service.generate_resume_pdf(test_content, "Mike_Peterson")
    print(f"Test result: {result}")
    
    if result["success"]:
        print(f"File exists: {os.path.exists(result['filepath'])}")