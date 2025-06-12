import logging
from werkzeug.utils import secure_filename
import re

class ResumeService:
    def __init__(self, scraper, document_service, openai_service=None, pdf_service=None):
        """Initialize ResumeService with required dependencies"""
        self.scraper = scraper
        self.document_service = document_service
        self.openai_service = openai_service
        self.pdf_service = pdf_service
        self.logger = logging.getLogger(__name__)
        
        # Log initialization
        self.logger.info(f"ResumeService initialized with scraper={scraper is not None}, "
                        f"document_service={document_service is not None}, "
                        f"openai_service={openai_service is not None}, "
                        f"pdf_service={pdf_service is not None}")

    def process_job_url(self, url):
        """Process a job URL with intelligent fallbacks and URL fixing"""
        try:
            self.logger.info(f"Processing job URL: {url}")
            
            # Fix common URL issues
            fixed_url = self._fix_common_url_issues(url)
            if fixed_url != url:
                self.logger.info(f"Fixed URL from {url} to {fixed_url}")
            
            # Extract job description
            job_description = self.scraper.extract_job_description(fixed_url)
            
            return {
                "success": True,
                "job_description": job_description,
                "message": f"Successfully extracted {len(job_description)} characters from job posting",
                "url_used": fixed_url,
                "extraction_length": len(job_description)
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to extract job description from {url}: {str(e)}")
            
            # Provide helpful error messages based on the site and error
            error_message = self._get_helpful_error_message(url, str(e))
            
            return {
                "success": False,
                "job_description": "",
                "message": error_message,
                "error": str(e),
                "url_used": url
            }

    def _fix_common_url_issues(self, url):
        """Fix common URL format issues"""
        # Fix LinkedIn collections URLs
        if "linkedin.com/jobs/collections" in url and "currentJobId=" in url:
            job_id_match = re.search(r'currentJobId=(\d+)', url)
            if job_id_match:
                job_id = job_id_match.group(1)
                fixed_url = f"https://www.linkedin.com/jobs/view/{job_id}"
                self.logger.info(f"Fixed LinkedIn collections URL to direct job URL")
                return fixed_url
        
        # Add more URL fixes as needed
        return url

    def _get_helpful_error_message(self, url, error):
        """Provide helpful error messages based on the site and error"""
        if "linkedin.com" in url:
            if "403" in error or "forbidden" in error.lower():
                return "LinkedIn is blocking automated access. Please copy and paste the job description manually."
            elif "page not found" in error.lower() or "404" in error:
                return "LinkedIn job posting not found. Please check the URL and try again, or copy the job description manually."
            else:
                return "LinkedIn job extraction failed. Please copy and paste the job description manually."
        
        elif "indeed.com" in url:
            if "403" in error or "forbidden" in error.lower():
                return "Indeed is blocking automated access. Please copy and paste the job description manually."
            else:
                return "Indeed job extraction failed. Please copy and paste the job description manually."
        
        elif "glassdoor.com" in url:
            return "Glassdoor job extraction failed. Please copy and paste the job description manually."
        
        else:
            return f"Could not extract job description from this site. Please copy and paste the job description manually."

    def process_resume(self, resume_file, job_description=None, job_url=None):
        """Process resume with job description or URL"""
        try:
            # Extract text from resume
            resume_filename = secure_filename(resume_file.filename)
            resume_text = self.document_service.extract_text_from_file(resume_file)
            
            # Get job description from URL if provided
            url_result = None
            if job_url and not job_description:
                url_result = self.process_job_url(job_url)
                
                if url_result["success"]:
                    job_description = url_result["job_description"]
                    self.logger.info(f"Successfully extracted job description from URL: {len(job_description)} characters")
                else:
                    # Return the error so the UI can handle it gracefully
                    return {
                        "success": False,
                        "message": url_result["message"],
                        "suggestion": "Please copy and paste the job description in the text area below.",
                        "url_error": True,
                        "url_result": url_result
                    }
            
            # Validate we have a job description
            if not job_description or len(job_description.strip()) < 50:
                return {
                    "success": False,
                    "message": "Please provide a job description (at least 50 characters) or a valid job URL"
                }
            
            # Process the resume and job description
            analysis_result = self._analyze_resume_vs_job(resume_text, job_description)
            
            return {
                "success": True,
                "resume_filename": resume_filename,
                "resume_text": resume_text,
                "job_description": job_description,
                "analysis": analysis_result,
                "url_result": url_result,
                "message": "Resume processed successfully!"
            }
            
        except Exception as e:
            self.logger.error(f"Error processing resume: {str(e)}")
            return {
                "success": False,
                "message": f"Error processing resume: {str(e)}"
            }

    def _analyze_resume_vs_job(self, resume_text, job_description):
        """Analyze resume against job description"""
        resume_words = len(resume_text.split())
        job_words = len(job_description.split())
        
        # Simple keyword matching
        job_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(resume_text)
        
        matching_keywords = set(job_keywords) & set(resume_keywords)
        
        return {
            "resume_word_count": resume_words,
            "job_word_count": job_words,
            "job_keywords": job_keywords[:10],  # Top 10 keywords
            "resume_keywords": resume_keywords[:10],
            "matching_keywords": list(matching_keywords)[:10],
            "match_percentage": len(matching_keywords) / len(job_keywords) * 100 if job_keywords else 0
        }

    def _extract_keywords(self, text):
        """Extract keywords from text"""
        # Convert to lowercase and split
        words = text.lower().split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        # Filter words and count frequency
        word_freq = {}
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w]', '', word)
            if len(clean_word) > 3 and clean_word not in stop_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Return top keywords sorted by frequency
        return sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)

    def generate_tailored_resume(self, user_info, job_description=None, job_url=None):
        """Generate a new resume from scratch using AI"""
        try:
            self.logger.info("Starting resume generation process")
            
            # Get job description from URL if provided
            url_result = None
            if job_url and not job_description:
                url_result = self.process_job_url(job_url)
                if url_result["success"]:
                    job_description = url_result["job_description"]
                else:
                    return {
                        "success": False,
                        "message": url_result["message"]
                    }
            
            if not job_description:
                return {
                    "success": False,
                    "message": "Please provide a job description or valid job URL"
                }
            
            if not self.openai_service:
                return {
                    "success": False,
                    "message": "OpenAI service not available. Please check your API key."
                }
            
            # Extract user name for file naming
            user_name = self._extract_user_name(user_info)
            
            # Generate resume using AI
            generated_resume = self.openai_service.generate_resume(user_info, job_description)
            
            # Generate PDF of the resume
            pdf_result = None
            if self.pdf_service:
                pdf_result = self.pdf_service.generate_resume_pdf(generated_resume, user_name)
            
            # Automatically generate cover letter
            cover_letter_result = self.generate_cover_letter(
                user_info=user_info,
                job_description=job_description,
                company_name=self._extract_company_name(job_description)
            )
            
            return {
                "success": True,
                "generated_resume": generated_resume,
                "job_description": job_description,
                "message": "Resume generated successfully!",
                "pdf_result": pdf_result,
                "cover_letter_result": cover_letter_result,
                "user_name": user_name
            }
            
        except Exception as e:
            self.logger.error(f"Error generating resume: {str(e)}")
            return {
                "success": False,
                "message": f"Error generating resume: {str(e)}"
            }

    def generate_cover_letter(self, user_info, job_description=None, job_url=None, company_name=None):
        """Generate a cover letter using AI"""
        try:
            # Get job description from URL if provided
            if job_url and not job_description:
                url_result = self.process_job_url(job_url)
                if url_result["success"]:
                    job_description = url_result["job_description"]
                else:
                    return {
                        "success": False,
                        "message": url_result["message"]
                    }
            
            if not job_description:
                return {
                    "success": False,
                    "message": "Please provide a job description or valid job URL"
                }
            
            if not self.openai_service:
                return {
                    "success": False,
                    "message": "OpenAI service not available. Please check your API key."
                }
            
            # Extract user name for file naming
            user_name = self._extract_user_name(user_info)
            
            # Generate cover letter using AI
            generated_cover_letter = self.openai_service.generate_cover_letter(
                user_info, job_description, company_name
            )
            
            # Generate PDF of the cover letter
            pdf_result = None
            if self.pdf_service:
                pdf_result = self.pdf_service.generate_cover_letter_pdf(generated_cover_letter, user_name)
            
            return {
                "success": True,
                "generated_cover_letter": generated_cover_letter,
                "job_description": job_description,
                "message": "Cover letter generated successfully!",
                "pdf_result": pdf_result,
                "user_name": user_name
            }
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter: {str(e)}")
            return {
                "success": False,
                "message": f"Error generating cover letter: {str(e)}"
            }

    def analyze_generated_resume(self, resume_content, job_description):
        """Analyze the quality of a generated resume against the job description"""
        try:
            if not self.openai_service:
                return {
                    "success": False,
                    "message": "OpenAI service not available. Please check your API key."
                }
            
            # Use OpenAI to analyze the resume
            analysis = self.openai_service.analyze_resume_fit(resume_content, job_description)
            
            # Also do basic keyword analysis
            basic_analysis = self._analyze_resume_vs_job(resume_content, job_description)
            
            return {
                "success": True,
                "ai_analysis": analysis,
                "keyword_analysis": basic_analysis,
                "message": "Resume analysis completed successfully!"
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing generated resume: {str(e)}")
            return {
                "success": False,
                "message": f"Error analyzing resume: {str(e)}"
            }

    def _extract_user_name(self, user_info):
        """Extract user name from user info for file naming"""
        # Look for name in the user_info string
        lines = user_info.split('\n')
        for line in lines:
            if 'Name:' in line:
                return line.replace('Name:', '').strip()
        
        # Fallback to first line or default
        first_line = lines[0].strip() if lines else "User"
        return first_line.replace('Name:', '').strip() or "User"

    def _extract_company_name(self, job_description):
        """Try to extract company name from job description"""
        # Simple extraction - look for common patterns
        lines = job_description.split('\n')[:10]  # Check first 10 lines
        
        for line in lines:
            # Look for patterns like "Company: XYZ" or "XYZ is looking for"
            if 'company:' in line.lower():
                return line.split(':')[1].strip()
            elif 'is looking for' in line.lower():
                return line.split('is looking for')[0].strip()
        
        return None
