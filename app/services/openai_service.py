from openai import OpenAI

class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def tailor_resume(self, resume_text, job_description, temperature=0.7, max_tokens=1000):
        """Tailor resume content to match job description."""
        prompt = self._create_resume_prompt(resume_text, job_description)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return True, response.choices[0].message.content
            
        except Exception as e:
            return False, f"Error from OpenAI: {str(e)}"
    
    def generate_cover_letter(self, resume_text, job_description, company_name="", tone="professional"):
        """Generate a cover letter based on resume and job description."""
        prompt = self._create_cover_letter_prompt(resume_text, job_description, company_name, tone)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            return True, response.choices[0].message.content
            
        except Exception as e:
            return False, f"Error generating cover letter: {str(e)}"
    
    def _create_resume_prompt(self, resume_text, job_description):
        """Create prompt for resume tailoring."""
        return (
            "You're an expert career coach. Using the job description below, tailor the resume content provided "
            "to better align with the job requirements. Focus on keywords and relevance. Do not fabricate experience, "
            "but emphasize related achievements.\n\n"
            f"Job Description:\n{job_description}\n\nResume:\n{resume_text}\n\nTailored Resume:"
        )
    
    def _create_cover_letter_prompt(self, resume_text, job_description, company_name, tone):
        """Create prompt for cover letter generation."""
        company_text = f" at {company_name}" if company_name else ""
        
        return (
            f"Create a compelling {tone} cover letter for this job application{company_text}. "
            "Use the resume information to highlight relevant experience and skills that match the job requirements. "
            "Make it engaging and specific to the role.\n\n"
            f"Job Description:\n{job_description}\n\n"
            f"Resume Information:\n{resume_text}\n\n"
            "Cover Letter:"
        )