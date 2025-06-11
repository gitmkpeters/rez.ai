import logging
from werkzeug.utils import secure_filename
import re

class ResumeService:
    def __init__(self, scraper, document_service, openai_service=None):
        self.scraper = scraper
        self.document_service = document_service
        self.openai_service = openai_service
        self.logger = logging.getLogger(__name__)

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
        """Analyze resume against job description (placeholder for now)"""
        # TODO: Add your AI/ML analysis logic here
        # For now, return basic statistics
        
        resume_words = len(resume_text.split())
        job_words = len(job_description.split())
        
        # Simple keyword matching (you can enhance this)
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
        """Extract keywords from text (simple implementation)"""
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
            
            # Generate resume using AI
            generated_resume = self.openai_service.generate_resume(user_info, job_description)
            
            return {
                "success": True,
                "generated_resume": generated_resume,
                "job_description": job_description,
                "message": "Resume generated successfully!"
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
            
            # Generate cover letter using AI
            generated_cover_letter = self.openai_service.generate_cover_letter(
                user_info, job_description, company_name
            )
            
            return {
                "success": True,
                "generated_cover_letter": generated_cover_letter,
                "job_description": job_description,
                "message": "Cover letter generated successfully!"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter: {str(e)}")
            return {
                "success": False,
                "message": f"Error generating cover letter: {str(e)}"
            }
