import os
import docx
from PyPDF2 import PdfReader

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed."""
    return os.path.splitext(filename)[1].lower() in allowed_extensions

def extract_text_from_file(filepath):
    """Extract text from uploaded files."""
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding='utf-8') as f:
            return f.read()
    return ""