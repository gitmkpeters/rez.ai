"""
Fix the download system to properly locate generated files
"""
import os
import shutil

def update_download_route():
    """Update the download route in main.py to check multiple directories"""
    
    # Read the current main.py
    with open("app/routes/main.py", "r") as f:
        content = f.read()
    
    # Find the download_pdf function and replace it
    new_download_function = '''@main_bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    """Download generated files with robust path handling"""
    try:
        # List of possible directories to check (in order of preference)
        possible_paths = [
            os.path.join('app/output', filename),      # PDF files location
            os.path.join('output', filename),          # Text files location
            os.path.join('app/static/output', filename),
            os.path.join('.', filename),               # Current directory
            filename                                   # Just filename
        ]
        
        # Try each possible location
        for file_path in possible_paths:
            if os.path.exists(file_path):
                logger.info(f"File found at: {file_path}")
                file_size = os.path.getsize(file_path)
                logger.info(f"File size: {file_size} bytes")
                
                # Determine the correct mimetype
                if filename.endswith('.pdf'):
                    mimetype = 'application/pdf'
                elif filename.endswith('.txt'):
                    mimetype = 'text/plain'
                else:
                    mimetype = 'application/octet-stream'
                
                return send_file(file_path, as_attachment=True, mimetype=mimetype)
        
        # If file not found in any location, list what files we do have
        logger.error(f"File not found: {filename}")
        
        # Debug: List files in all directories
        for directory in ['output', 'app/output', 'app/static/output']:
            if os.path.exists(directory):
                files = os.listdir(directory)
                logger.info(f"Files in {directory}: {files}")
        
        flash('File not found. It may have been moved or deleted.', 'error')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('main.index'))'''
    
    # Replace the existing download_pdf function
    import re
    pattern = r'@main_bp\.route$$\'/download-pdf/<filename>\'$$.*?return redirect$$url_for\(\'main\.index\'$$\)'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_download_function, content, flags=re.DOTALL)
        
        # Write the updated content back
        with open("app/routes/main.py", "w") as f:
            f.write(content)
        
        print("✅ Updated download_pdf function in main.py")
        return True
    else:
        print("❌ Could not find download_pdf function to replace")
        return False

def test_file_locations():
    """Test what files exist in different directories"""
    print("\n=== Current File Locations ===")
    
    directories = ['output', 'app/output', 'app/static/output']
    
    for directory in directories:
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"\n{directory}/:")
            for file in files:
                file_path = os.path.join(directory, file)
                size = os.path.getsize(file_path)
                print(f"  - {file} ({size} bytes)")
        else:
            print(f"\n{directory}/: (does not exist)")

if __name__ == "__main__":
    print("=== Fixing Download System ===")
    
    # Test current file locations
    test_file_locations()
    
    # Update the download route
    if update_download_route():
        print("\n✅ Download system updated successfully!")
        print("\nNext steps:")
        print("1. Restart your Flask app")
        print("2. Generate a new resume")
        print("3. Try downloading the file")
    else:
        print("\n❌ Failed to update download system")
        print("Manual update may be required")
