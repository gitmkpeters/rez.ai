import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_directory(directory_path):
    """Ensure a directory exists, create it if it doesn't"""
    try:
        if not os.path.exists(directory_path):
            logger.info(f"Creating directory: {directory_path}")
            os.makedirs(directory_path, exist_ok=True)
        
        # Test if directory is writable
        test_file = os.path.join(directory_path, "test_write.txt")
        with open(test_file, "w") as f:
            f.write("Test write access")
        os.remove(test_file)
        logger.info(f"Directory {directory_path} exists and is writable")
        return True
    except Exception as e:
        logger.error(f"Error with directory {directory_path}: {str(e)}")
        return False

# Directories to check/create
directories = [
    "output",                # Root level output directory
    "app/output",            # App-level output directory
    "uploads",               # For uploaded files
    "app/uploads",           # Alternative uploads location
    "debug_html",            # For debug HTML files
    "app/static",            # Static files directory
    "app/static/output"      # Another possible output location
]

# Check all directories
all_success = True
for directory in directories:
    if not ensure_directory(directory):
        all_success = False

if all_success:
    print("All directories created and writable!")
else:
    print("Some directories could not be created or are not writable. Check the logs.")
