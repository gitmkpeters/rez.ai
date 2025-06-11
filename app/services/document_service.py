# app/services/document_service.py

import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from docx import Document
import PyPDF2
from werkzeug.datastructures import FileStorage

class DocumentService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Use absolute paths from the project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.upload_folder = os.path.join(project_root, 'uploads')
        self.output_folder = os.path.join(project_root, 'output')
        
        # Create directories if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        print(f"DocumentService - Upload folder: {self.upload_folder}")
        print(f"DocumentService - Output folder: {self.output_folder}")
            
    def extract_text_from_file(self, file):
        """Extract text from uploaded file"""
        try:
            filename = file.filename.lower()
            
            if filename.endswith('.pdf'):
                return self._extract_from_pdf(file)
            elif filename.endswith('.docx'):
                return self._extract_from_docx(file)
            elif filename.endswith('.txt'):
                return self._extract_from_txt(file)
            else:
                raise ValueError("Unsupported file format")
                
        except Exception as e:
            self.logger.error(f"Error extracting text from file: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
    
    def _extract_from_docx(self, file):
        """Extract text from DOCX file"""
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")
    
    def _extract_from_txt(self, file):
        """Extract text from TXT file"""
        try:
            return file.read().decode('utf-8').strip()
        except Exception as e:
            raise ValueError(f"Error reading TXT file: {str(e)}")
    
    def generate_pdf(self, content, filename):
        """Generate PDF from text content"""
        try:
            output_path = os.path.join(self.output_folder, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Create custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
            )
            
            # Build PDF content
            story = []
            
            # Split content into sections
            sections = content.split('\n\n')
            
            for i, section in enumerate(sections):
                if section.strip():
                    if i == 0:  # First section as title
                        story.append(Paragraph(section.strip(), title_style))
                    else:
                        story.append(Paragraph(section.strip(), normal_style))
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}")
            raise ValueError(f"Error generating PDF: {str(e)}")