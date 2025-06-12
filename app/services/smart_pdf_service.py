import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from datetime import datetime
import re
import traceback

class SmartPDFService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_resume_pdf(self, resume_content, user_name="Resume", output_dir="app/output"):
        """Generate a well-formatted PDF from resume content with smart placeholder filtering"""
        try:
            self.logger.info(f"Starting smart PDF generation for resume: {user_name}")
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Resume_{timestamp}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            # Create PDF document with better margins
            doc = SimpleDocTemplate(
                filepath, 
                pagesize=letter,
                rightMargin=0.75*inch, 
                leftMargin=0.75*inch,
                topMargin=0.75*inch, 
                bottomMargin=0.75*inch
            )
            
            # Get and customize styles
            styles = self._get_custom_styles()
            
            # Clean the content for resume (more aggressive placeholder removal)
            cleaned_content = self._remove_resume_placeholders(resume_content)
            
            # Build content
            story = []
            
            # Parse and format the resume content
            self.logger.info("Parsing and formatting resume content")
            formatted_sections = self._parse_and_format_resume(cleaned_content)
            
            # Add each section to the story
            for section in formatted_sections:
                if section['type'] == 'header':
                    story.append(Paragraph(section['content'], styles['header']))
                    story.append(Spacer(1, 12))
                elif section['type'] == 'contact':
                    story.append(Paragraph(section['content'], styles['contact']))
                    story.append(Spacer(1, 16))
                elif section['type'] == 'section_title':
                    story.append(Spacer(1, 8))
                    story.append(Paragraph(section['content'], styles['section_title']))
                    story.append(Spacer(1, 6))
                elif section['type'] == 'content':
                    story.append(Paragraph(section['content'], styles['body']))
                    story.append(Spacer(1, 6))
                elif section['type'] == 'bullet':
                    story.append(Paragraph(section['content'], styles['bullet']))
                    story.append(Spacer(1, 3))
            
            # Build PDF
            self.logger.info("Building PDF document")
            doc.build(story)
            
            # Verify file was created
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                self.logger.info(f"✅ PDF generated successfully: {filepath} ({file_size} bytes)")
                
                return {
                    "success": True,
                    "filepath": filepath,
                    "filename": filename,
                    "message": f"PDF generated successfully as {filename}",
                    "file_size": file_size
                }
            else:
                raise Exception("PDF file was not created")
            
        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "message": f"Error generating PDF: {str(e)}"
            }
    
    def generate_cover_letter_pdf(self, cover_letter_content, user_name="Cover_Letter", output_dir="app/output"):
        """Generate a well-formatted cover letter PDF with minimal placeholder removal"""
        try:
            self.logger.info(f"Starting cover letter PDF generation for: {user_name}")
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            safe_name = re.sub(r'[^\w\s-]', '', user_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_Cover_Letter_{timestamp}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath, 
                pagesize=letter,
                rightMargin=0.75*inch, 
                leftMargin=0.75*inch,
                topMargin=0.75*inch, 
                bottomMargin=0.75*inch
            )
            
            # Get styles
            styles = self._get_custom_styles()
            
            # Clean the content for cover letter (minimal placeholder removal)
            cleaned_content = self._clean_cover_letter_content(cover_letter_content)
            
            # Build content
            story = []
            
            # Add date
            today = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(today, styles['date']))
            story.append(Spacer(1, 24))
            
            # Format cover letter content
            paragraphs = self._format_cover_letter_content(cleaned_content)
            
            for para in paragraphs:
                if para.strip():
                    clean_para = self._clean_text_for_pdf(para.strip())
                    story.append(Paragraph(clean_para, styles['body']))
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            # Verify file was created
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                self.logger.info(f"✅ Cover letter PDF generated: {filepath} ({file_size} bytes)")
                
                return {
                    "success": True,
                    "filepath": filepath,
                    "filename": filename,
                    "message": f"Cover letter PDF generated as {filename}",
                    "file_size": file_size
                }
            else:
                raise Exception("Cover letter PDF file was not created")
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter PDF: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "message": f"Error generating cover letter PDF: {str(e)}"
            }
    
    def _remove_resume_placeholders(self, content):
        """Remove common placeholder text from resume content (more aggressive)"""
        # List of common placeholder patterns for resumes
        placeholder_patterns = [
            r'\[Your Name\]',
            r'\[Company Name\]',
            r'\[Location\]',
            r'\[Dates\]',
            r'\[City, State, Zip Code\]',
            r'\[Email Address\]',
            r'\[Phone Number\]',
            r'\[Your Address\]',
            r'\[Degree Earned\]',
            r'\[Graduation Year\]'
        ]
        
        # Replace each placeholder with empty string
        cleaned_content = content
        for pattern in placeholder_patterns:
            cleaned_content = re.sub(pattern, '', cleaned_content)
        
        # Remove any lines that are now empty or just whitespace
        lines = cleaned_content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return '\n'.join(non_empty_lines)
    
    def _clean_cover_letter_content(self, content):
        """Clean cover letter content with minimal placeholder removal"""
        # For cover letters, only remove obvious unfilled placeholders
        # Don't remove placeholders that might be part of the content structure
        
        # Remove only clearly unfilled placeholders (those that appear standalone)
        unfilled_patterns = [
            r'^\[Your Name\]$',
            r'^\[Your Address\]$',
            r'^\[City, State, Zip Code\]$',
            r'^\[Email Address\]$',
            r'^\[Phone Number\]$',
            r'^\[Date\]$'
        ]
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            should_remove = False
            
            # Check if this line is an unfilled placeholder
            for pattern in unfilled_patterns:
                if re.match(pattern, line_stripped):
                    should_remove = True
                    break
            
            if not should_remove:
                cleaned_lines.append(line)
        
        # Also clean up any trailing metadata or instructions
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Remove any trailing instructions or metadata
        if "---" in cleaned_content:
            cleaned_content = cleaned_content.split("---")[0].strip()
        
        # Remove any lines that start with "This cover letter"
        lines = cleaned_content.split('\n')
        final_lines = []
        for line in lines:
            if not line.strip().startswith("This cover letter"):
                final_lines.append(line)
        
        return '\n'.join(final_lines)
    
    def _get_custom_styles(self):
        """Create custom styles for the PDF"""
        styles = getSampleStyleSheet()
        
        custom_styles = {
            'header': ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=6,
                alignment=TA_CENTER,
                textColor=HexColor('#2c3e50'),
                fontName='Helvetica-Bold'
            ),
            'contact': ParagraphStyle(
                'ContactInfo',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                alignment=TA_CENTER,
                textColor=HexColor('#34495e')
            ),
            'section_title': ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                spaceBefore=12,
                textColor=HexColor('#2c3e50'),
                fontName='Helvetica-Bold',
                borderWidth=1,
                borderColor=HexColor('#bdc3c7'),
                borderPadding=3
            ),
            'body': ParagraphStyle(
                'BodyText',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                alignment=TA_JUSTIFY,
                leading=14
            ),
            'bullet': ParagraphStyle(
                'BulletPoint',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=3,
                leftIndent=20,
                bulletIndent=10,
                leading=13
            ),
            'date': ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=24,
                alignment=TA_LEFT
            )
        }
        
        return custom_styles
    
    def _parse_and_format_resume(self, content):
        """Parse resume content into properly formatted sections"""
        sections = []
        lines = content.split('\n')
        
        # Extract name (usually first line)
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 100 and not any(word in first_line.lower() for word in ['experience', 'education', 'skills', 'summary']):
                sections.append({
                    'type': 'header',
                    'content': first_line
                })
                lines = lines[1:]  # Remove the name line
        
        # Extract contact information (look for email, phone, etc.)
        contact_lines = []
        content_start_idx = 0
        
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            line_lower = line.lower().strip()
            if any(indicator in line_lower for indicator in ['@', 'phone', 'email', 'linkedin', 'github', '.com']):
                contact_lines.append(line.strip())
                content_start_idx = i + 1
            elif line.strip() and not contact_lines:
                # If we hit content without finding contact info, stop looking
                break
        
        if contact_lines:
            sections.append({
                'type': 'contact',
                'content': ' | '.join(contact_lines)
            })
        
        # Process remaining content
        remaining_content = '\n'.join(lines[content_start_idx:])
        content_sections = self._identify_resume_sections(remaining_content)
        
        for section_name, section_content in content_sections.items():
            if section_content.strip():
                # Add section title
                sections.append({
                    'type': 'section_title',
                    'content': section_name.upper()
                })
                
                # Process section content
                section_parts = self._format_section_content(section_content)
                sections.extend(section_parts)
        
        return sections
    
    def _identify_resume_sections(self, content):
        """Identify and extract different sections of the resume"""
        sections = {
            'Professional Summary': '',
            'Work Experience': '',
            'Education': '',
            'Skills': '',
            'Other': ''
        }
        
        # Common section headers to look for
        section_patterns = {
            'Professional Summary': ['summary', 'objective', 'profile', 'professional summary'],
            'Work Experience': ['experience', 'employment', 'work history', 'work experience', 'professional experience'],
            'Education': ['education', 'academic', 'qualifications'],
            'Skills': ['skills', 'technical skills', 'competencies', 'technologies']
        }
        
        # First, try to find explicit section headers
        lines = content.split('\n')
        current_section = 'Other'
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                current_content.append('')
                continue
            
            # Check if this line is a section header
            line_lower = line_stripped.lower()
            found_section = False
            
            for section_name, patterns in section_patterns.items():
                if any(pattern in line_lower for pattern in patterns) or line_lower == section_name.lower():
                    # Save previous section content
                    if current_content:
                        sections[current_section] += '\n'.join(current_content) + '\n'
                    
                    # Start new section
                    current_section = section_name
                    current_content = []
                    found_section = True
                    break
            
            if not found_section:
                current_content.append(line_stripped)
        
        # Save the last section
        if current_content:
            sections[current_section] += '\n'.join(current_content)
        
        return sections
    
    def _format_section_content(self, content):
        """Format section content into paragraphs and bullet points"""
        formatted_parts = []
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
            
            lines = paragraph.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if it's a bullet point
                if line.startswith(('-', '•', '*', '◦')) or line.startswith('- ') or line == '•':
                    # Format as bullet point - handle empty bullet points
                    if line == '•' or line == '-':
                        continue  # Skip empty bullet points
                        
                    bullet_text = line.lstrip('-•*◦ ').strip()
                    if bullet_text:  # Only add if there's actual content
                        formatted_parts.append({
                            'type': 'bullet',
                            'content': f"• {bullet_text}"
                        })
                else:
                    # Format as regular content
                    formatted_parts.append({
                        'type': 'content',
                        'content': self._clean_text_for_pdf(line)
                    })
        
        return formatted_parts
    
    def _format_cover_letter_content(self, content):
        """Format cover letter content into proper paragraphs"""
        # Split by double newlines to get paragraphs
        paragraphs = content.split('\n\n')
        
        # Clean up paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            # Replace single newlines with spaces within paragraphs
            cleaned_para = ' '.join(para.split('\n'))
            cleaned_para = cleaned_para.strip()
            if cleaned_para:
                cleaned_paragraphs.append(cleaned_para)
        
        return cleaned_paragraphs
    
    def _clean_text_for_pdf(self, text):
        """Clean text for PDF generation - escape special characters"""
        if not text:
            return ""
        
        # Replace problematic characters for ReportLab
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        
        # Handle bullet points
        text = text.replace('•', '&#8226;')
        
        # Handle em dashes and en dashes
        text = text.replace('—', '&#8212;')
        text = text.replace('–', '&#8211;')
        
        return text