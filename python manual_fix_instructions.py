print("📝 Manual Fix Instructions")
print("=========================")
print("""
Since the automatic fix had syntax issues, here's how to manually fix the download route:

1. Open the file: app/routes/main.py

2. Find the download_pdf function (search for "@main_bp.route('/download-pdf/<filename>')")

3. Replace the entire function with this code:

@main_bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    \"\"\"Download generated files with robust path handling - FIXED VERSION\"\"\"
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
                
                # Use the absolute path with os.path.abspath
                abs_path = os.path.abspath(file_path)
                logger.info(f"Serving absolute path: {abs_path}")
                return send_file(abs_path, as_attachment=True, mimetype=mimetype)
        
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

4. Save the file and restart your Flask application
""")
