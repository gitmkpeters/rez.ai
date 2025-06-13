#!/usr/bin/env python3
"""
One-Step ATS Optimization Fix

This script directly adds the tailored summary feature to your OpenAI service
in the simplest possible way.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def add_tailored_summary_method():
    """Add the tailored summary method to OpenAIService in the simplest way possible"""
    
    # Path to the OpenAI service file
    service_path = os.path.join('app', 'services', 'openai_service.py')
    
    if not os.path.exists(service_path):
        logger.error(f"❌ OpenAI service file not found at {service_path}")
        return False
    
    # Read the current file
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Check if the method already exists
    if 'def generate_tailored_summary' in content:
        logger.info("✅ generate_tailored_summary method already exists")
        return True
    
    # Create a backup
    backup_path = f"{service_path}.bak"
    with open(backup_path, 'w') as f:
        f.write(content)
    logger.info(f"✅ Created backup at {backup_path}")
    
    # Find the class definition
    class_def = "class OpenAIService:"
    if class_def not in content:
        logger.error("❌ OpenAIService class definition not found")
        return False
    
    # Add the new method at the end of the file
    new_method = """

    def generate_tailored_summary(self, work_experience, job_description, user_skills=None):
        \"\"\"Generate a highly tailored professional summary optimized for ATS and job matching\"\"\"
        try:
            # Extract key information for better targeting
            skills_text = f"\\n\\nKey Skills: {user_skills}" if user_skills else ""
            
            prompt = f\"\"\"
            You are an expert ATS optimization specialist and resume writer. Create a powerful, tailored professional summary that will achieve the HIGHEST possible match score with the job description.

            JOB DESCRIPTION TO MATCH:
            {job_description}

            USER'S WORK EXPERIENCE:
            {work_experience}{skills_text}

            Create a professional summary (3-4 sentences, 80-120 words) that:

            1. **KEYWORD OPTIMIZATION**: Include the EXACT keywords and phrases from the job description
            2. **QUANTIFIED ACHIEVEMENTS**: Use specific numbers, percentages, or metrics from the user's experience
            3. **ROLE ALIGNMENT**: Mirror the job title and key responsibilities mentioned in the posting
            4. **INDUSTRY LANGUAGE**: Use the same terminology and buzzwords as the job description
            5. **VALUE PROPOSITION**: Clearly state how the candidate solves the employer's specific needs
            6. **ATS FRIENDLY**: Use standard formatting and avoid special characters

            REQUIREMENTS:
            - Start with the candidate's years of experience and primary expertise area
            - Include 3-5 key skills/technologies mentioned in the job posting
            - Mention 1-2 quantified achievements that align with job requirements
            - End with a forward-looking statement about contributing to the company's goals
            - Use action verbs that match the job description's language
            - Ensure every word adds value for ATS scanning

            Return ONLY the professional summary text, no additional formatting or explanations.
            \"\"\"
            
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for better quality
                messages=[
                    {"role": "system", "content": "You are an expert ATS optimization specialist who creates professional summaries that achieve maximum job match scores."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3  # Lower temperature for more focused, consistent output
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Log for debugging
            self.logger.info(f"Generated tailored summary: {len(summary)} characters")
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating tailored summary: {str(e)}")
            raise ValueError(f"Error generating tailored summary: {str(e)}")
"""
    
    # Append the new method to the file
    with open(service_path, 'a') as f:
        f.write(new_method)
    
    logger.info("✅ Successfully added generate_tailored_summary method")
    
    # Add a simple test function to the resume_service.py file
    resume_service_path = os.path.join('app', 'services', 'resume_service.py')
    
    if os.path.exists(resume_service_path):
        with open(resume_service_path, 'r') as f:
            resume_content = f.read()
        
        # Add helper methods if they don't exist
        if '_extract_work_experience' not in resume_content:
            helper_methods = """
    def _extract_work_experience(self, user_info):
        \"\"\"Extract work experience section from user info\"\"\"
        lines = user_info.split('\\n')
        experience_section = []
        in_experience = False
        
        for line in lines:
            if 'Work Experience:' in line or 'Employment:' in line or 'Experience:' in line:
                in_experience = True
                continue
            elif in_experience and any(section in line for section in ['Education:', 'Skills:', 'Name:', 'Email:', 'Phone:']):
                break
            elif in_experience:
                experience_section.append(line)
        
        return '\\n'.join(experience_section).strip()

    def _extract_skills(self, user_info):
        \"\"\"Extract skills section from user info\"\"\"
        lines = user_info.split('\\n')
        skills_section = []
        in_skills = False
        
        for line in lines:
            if 'Skills:' in line or 'Technical Skills:' in line or 'Core Competencies:' in line:
                in_skills = True
                continue
            elif in_skills and any(section in line for section in ['Work Experience:', 'Education:', 'Name:', 'Email:', 'Phone:']):
                break
            elif in_skills:
                skills_section.append(line)
        
        return '\\n'.join(skills_section).strip()
"""
            # Create a backup
            backup_path = f"{resume_service_path}.bak"
            with open(backup_path, 'w') as f:
                f.write(resume_content)
            logger.info(f"✅ Created backup of resume service at {backup_path}")
            
            # Append the helper methods
            with open(resume_service_path, 'a') as f:
                f.write(helper_methods)
            
            logger.info("✅ Added helper methods to ResumeService")
    
    # Create a simple test script
    test_script = """#!/usr/bin/env python3
\"\"\"
Simple ATS Test

This script tests the tailored summary generation.
\"\"\"

import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def test_tailored_summary():
    \"\"\"Test the tailored summary generation\"\"\"
    print("\\n🚀 Testing Tailored Summary Generation\\n")
    
    try:
        # Import the services
        from app.services import openai_service
        
        # Sample job description
        job_description = \"\"\"
        Senior Software Engineer

        We are looking for a Senior Software Engineer with 5+ years of experience in Python and web development.
        The ideal candidate will have experience with React, Node.js, and cloud technologies (AWS preferred).
        You will be responsible for designing, developing, and maintaining web applications, collaborating with
        cross-functional teams, and mentoring junior developers.

        Requirements:
        - 5+ years of experience in software development
        - Strong proficiency in Python and JavaScript
        - Experience with React, Node.js, and modern frontend frameworks
        - Knowledge of database systems (SQL and NoSQL)
        - Experience with AWS or other cloud platforms
        - Excellent problem-solving and communication skills
        \"\"\"
        
        # Sample work experience
        work_experience = \"\"\"
        Senior Software Engineer, TechCorp (2018-Present)
        - Led development of cloud-based applications using Python and AWS
        - Improved application performance by 40% through code optimization
        - Managed a team of 5 junior developers on multiple projects
        - Implemented CI/CD pipelines reducing deployment time by 60%

        Software Developer, InnovateSoft (2015-2018)
        - Developed web applications using React, Node.js, and MongoDB
        - Created RESTful APIs for mobile application backend
        - Collaborated with UX designers to implement responsive interfaces
        \"\"\"
        
        # Sample skills
        skills = "Python, JavaScript, React, Node.js, AWS, MongoDB, CI/CD, Docker, Kubernetes"
        
        # Generate tailored summary
        print("Generating tailored summary...")
        summary = openai_service.generate_tailored_summary(
            work_experience=work_experience,
            job_description=job_description,
            user_skills=skills
        )
        
        print("\\n✅ GENERATED TAILORED SUMMARY:\\n")
        print(summary)
        print("\\n")
        
        # Save the summary to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"tailored_summary_{timestamp}.txt"
        
        with open(output_file, "w") as f:
            f.write(summary)
        
        print(f"Summary saved to {output_file}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_tailored_summary()
"""
    
    # Write the test script
    test_script_path = "test_summary.py"
    with open(test_script_path, 'w') as f:
        f.write(test_script)
    
    logger.info(f"✅ Created test script at {test_script_path}")
    
    return True

if __name__ == "__main__":
    print("🚀 One-Step ATS Optimization Fix")
    print("=" * 50)
    
    if add_tailored_summary_method():
        print("\n✅ SUCCESS! The tailored summary feature has been added.")
        print("\nTo test it, restart your Flask application and run:")
        print("python test_summary.py")
        print("\nThis will generate a tailored summary using your OpenAI service.")
    else:
        print("\n❌ Failed to add the tailored summary feature.")
        print("Please check the error messages above.")
