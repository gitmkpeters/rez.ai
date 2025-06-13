import os
import shutil
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_download_route():
    """Fix the download route in main.py"""
    try:
        # Path to the main.py file
        main_py_path = "app/routes/main.py"
        backup_path = "app/routes/main.py.bak"
        
        # Create a backup
        shutil.copy2(main_py_path, backup_path)
        logger.info(f"Created backup of main.py at {backup_path}")
        
        # Read the current content
        with open(main_py_path, 'r') as file:
            content = file.read()
        
        # Replace the problematic download_pdf function
        new_download_function = """
@main_bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    """Download generated files with robust path handling - FIXED VERSION"""
    try:
        logger.info(f"Download request for file: {filename}")
        
        # List of possible directories to check (in order of preference)
        possible_paths = [
            os.path.join('output', filename),          # Main output directory
            os.path.join('app/output', filename),      # App output directory
            os.path.join('app/static/output', filename),
            os.path.join('.', filename),               # Current directory
            filename                                   # Just filename
        ]
        
        # Try each possible location
        for file_path in possible_paths:
            if os.path.exists(file_path):
                logger.info(f"✅ File found at: {file_path}")
                file_size = os.path.getsize(file_path)
                logger.info(f"File size: {file_size} bytes")
                
                # Determine the correct mimetype
                if filename.endswith('.pdf'):
                    mimetype = 'application/pdf'
                elif filename.endswith('.txt'):
                    mimetype = 'text/plain'
                else:
                    mimetype = 'application/octet-stream'
                
                logger.info(f"Serving file with mimetype: {mimetype}")
                
                # Use the RELATIVE path, not absolute path
                return send_file(os.path.abspath(file_path), as_attachment=True, mimetype=mimetype)
        
        # If file not found in any location, list what files we do have
        logger.error(f"❌ File not found: {filename}")
        
        # Debug: List files in all directories
        for directory in ['output', 'app/output', 'app/static/output']:
            if os.path.exists(directory):
                files = os.listdir(directory)
                logger.info(f"Files in {directory}: {files}")
            else:
                logger.info(f"Directory {directory} does not exist")
        
        flash(f'File "{filename}" not found. It may have been moved or deleted.', 'error')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"❌ Error downloading file: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('main.index'))
"""
        
        # Find and replace the download_pdf function
        import re
        pattern = r'@main_bp\.route$$\'/download-pdf/<filename>\'$$(.*?)def download_pdf$$filename$$:(.*?)@main_bp\.route'
        replacement = f"@main_bp.route('/download-pdf/<filename>')\ndef download_pdf(filename):{new_download_function}@main_bp.route"
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write the updated content
        with open(main_py_path, 'w') as file:
            file.write(new_content)
        
        logger.info("✅ Successfully updated download_pdf function in main.py")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error fixing download route: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing download path issue...")
    if fix_download_route():
        print("✅ Download route fixed successfully!")
        print("🔄 Please restart your Flask application")
    else:
        print("❌ Failed to fix download route")
