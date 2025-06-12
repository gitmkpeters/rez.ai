import os
import logging
from datetime import datetime
import re

class SimplePDFService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # List of possible output directories in order of preference
        self.possible_dirs = [
            "output",
            "app/output",
            "app/static/output",
            "."  # Current directory as last resort
        ]
        
    def _get_working_directory(self):
        """Find a working directory from the list of possibilities"""
        for directory in self.possible_dirs:
            try:
                os.makedirs(directory, exist_ok=True)
                test_file = os.path.join(directory, "test_write.txt")
                with open(test_file, "w") as f:
                    f.write("Test write access")
                os.remove(test_file)
                self.logger.info(f"Using output directory: {directory}")
                return directory
            except Exception as e:
                self.logger.warning(f"Directory {directory} not usable: {str(e)}")
        
        # If no directory works, use current directory
        self.logger.warning("No output directory is writable, using current directory")
        return "."
        
    def generate_resume_pdf(self, resume_content, user_name="Resume"):
        """Generate a text file instead of PDF as a fallback"""
        try:
            self.logger.info(f"Starting text file generation for resume: {user_name}")
            
            # Get a working directory
            output_dir = self._get_working_directory()
            
            # Create filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Resume_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Write content to text file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(resume_content)
            
            self.logger.info(f"Text file generated successfully: {filepath}")
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "message": f"Resume saved as text file: {filename}"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating text file: {str(e)}")
            return {
                "success": False,
                "message": f"Error generating file: {str(e)}"
            }
    
    def generate_cover_letter_pdf(self, cover_letter_content, user_name="Cover_Letter"):
        """Generate a text file instead of PDF as a fallback"""
        try:
            self.logger.info(f"Starting text file generation for cover letter: {user_name}")
            
            # Get a working directory
            output_dir = self._get_working_directory()
            
            # Create filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Cover_Letter_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Write content to text file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cover_letter_content)
            
            self.logger.info(f"Text file generated successfully: {filepath}")
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "message": f"Cover letter saved as text file: {filename}"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating text file: {str(e)}")
            return {
                "success": False,
                "message": f"Error generating file: {str(e)}"
            }
