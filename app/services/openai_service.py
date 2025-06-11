import os
import logging
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.logger = logging.getLogger(__name__)
    
    def tailor_resume(self, resume_text, job_description):
        """Tailor existing resume content based on job description"""
        try:
            prompt = f"""
            You are a professional resume writer. Please tailor the following resume to better match the job description provided.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_description}

            Please rewrite the resume to:
            1. Highlight relevant skills and experiences that match the job requirements
            2. Use keywords from the job description where appropriate
            3. Reorganize content to emphasize the most relevant qualifications
            4. Maintain professional formatting and structure
            5. Keep all factual information accurate - do not add false experience

            Return only the tailored resume content, properly formatted for a professional document.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer with expertise in tailoring resumes for specific job applications."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error tailoring resume with OpenAI: {str(e)}")
            raise ValueError(f"Error processing resume with AI: {str(e)}")

    def generate_resume(self, user_info, job_description):
        """Generate a new resume from scratch based on user info and job description"""
        try:
            prompt = f"""
            You are a professional resume writer. Create a compelling resume based on the user information and job description provided.

            USER INFORMATION:
            {user_info}

            JOB DESCRIPTION:
            {job_description}

            Please create a professional resume that:
            1. Uses the user's actual information and experience
            2. Highlights skills and experiences most relevant to the job
            3. Incorporates keywords from the job description naturally
            4. Follows modern resume best practices
            5. Is formatted professionally with clear sections
            6. Does not fabricate experience - only reorganizes and emphasizes existing qualifications

            Return a complete, well-formatted resume ready for submission.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer who creates compelling, ATS-friendly resumes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating resume with OpenAI: {str(e)}")
            raise ValueError(f"Error generating resume with AI: {str(e)}")

    def generate_cover_letter(self, user_info, job_description, company_name=None):
        """Generate a cover letter based on user info and job description"""
        try:
            company_text = f" at {company_name}" if company_name else ""
            
            prompt = f"""
            You are a professional career counselor. Write a compelling cover letter based on the user information and job description provided.

            USER INFORMATION:
            {user_info}

            JOB DESCRIPTION:
            {job_description}

            Please create a cover letter that:
            1. Opens with a strong, engaging introduction
            2. Highlights the user's most relevant qualifications for this specific role
            3. Shows enthusiasm for the position{company_text}
            4. Uses specific examples from the user's background
            5. Incorporates keywords from the job description naturally
            6. Closes with a professional call to action
            7. Is concise but impactful (3-4 paragraphs)

            Return a complete, professional cover letter ready for submission.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career counselor who writes compelling, personalized cover letters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating cover letter with OpenAI: {str(e)}")
            raise ValueError(f"Error generating cover letter with AI: {str(e)}")

    def analyze_resume_fit(self, resume_text, job_description):
        """Analyze how well a resume fits a job and provide improvement suggestions"""
        try:
            prompt = f"""
            You are a hiring manager and resume expert. Analyze how well this resume matches the job description and provide specific improvement suggestions.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_description}

            Please provide:
            1. Overall fit score (1-10)
            2. Top 3 strengths that match the job
            3. Top 3 areas for improvement
            4. Specific keywords/skills missing from the resume
            5. Suggestions for better positioning of existing experience

            Format your response as a structured analysis.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert hiring manager who provides detailed resume feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error analyzing resume fit with OpenAI: {str(e)}")
            raise ValueError(f"Error analyzing resume with AI: {str(e)}")
