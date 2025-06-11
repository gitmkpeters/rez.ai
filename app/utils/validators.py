import re
from urllib.parse import urlparse

def validate_url(url):
    """Validate if URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_file_size(file, max_size_mb=16):
    """Validate file size."""
    if file:
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        return size <= max_size_mb * 1024 * 1024
    return False

def sanitize_filename(filename):
    """Sanitize filename for security."""
    # Remove any path components
    filename = os.path.basename(filename)
    # Remove or replace dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename