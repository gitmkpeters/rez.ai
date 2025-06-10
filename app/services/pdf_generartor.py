import html
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class PDFGeneratorService:
    """Service for generating PDF documents."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def create_resume_pdf(self, text, output_path):
        """Create a professional resume PDF from text."""
        try:
            doc = SimpleDocTemplate(
                output_path, 
                pagesize=letter,
                rightMargin=72, 
                leftMargin=72,
                topMargin=72, 
                bottomMargin=18
            )
            
            story = []
            
            # Split text into paragraphs
            paragraphs = text.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    # Clean up the text and handle basic formatting
                    clean_para = html.unescape(para.strip())
                    p = Paragraph(clean_para, self.styles['Normal'])
                    story.append(p)
                    story.append(Spacer(1, 12))
            
            doc.build(story)
            return True, f"PDF saved to {output_path}"
            
        except Exception as e:
            return False, f"Error creating PDF: {str(e)}"
    
    def create_cover_letter_pdf(self, text, output_path):
        """Create a cover letter PDF from text."""
        # Similar to resume but with different formatting
        return self.create_resume_pdf(text, output_path)