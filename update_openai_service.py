#!/usr/bin/env python3
"""
Update OpenAI Service

This script updates the OpenAIService class with new methods for ATS optimization.
"""

import os
import sys
import shutil
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('update_service')

def backup_file(file_path):
    """Create a backup of the file"""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.{timestamp}.bak"
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return True
    return False

def update_openai_service():
    """Update the OpenAIService class with new methods"""
    
    # Path to the OpenAIService file
    service_path = os.path.join('app', 'services', 'openai_service.py')
    
    if not os.path.exists(service_path):
        logger.error(f"OpenAIService file not found at {service_path}")
        return False
    
    # Create a backup
    if not backup_file(service_path):
        logger.error("Failed to create backup")
        return False
    
    # Read the current file
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Check if the method already exists
    if 'def generate_tailored_summary' in content:
        logger.info("generate_tailored_summary method already exists")
        return True
    
    # Find the class definition
    class_def = "class OpenAIService:"
    if class_def not in content:
        logger.error("OpenAIService class definition not found")
        return False
    
    # Find the last method in the class
    methods = [
        "def analyze_resume_fit",
        "def generate_cover_letter",
        "def generate_resume",
        "def tailor_resume",
        "def __init__"
    ]
    
    last_method_pos = -1
    last_method_name = ""
    
    for method in methods:
        pos = content.find(method)
        if pos > last_method_pos:
            last_method_pos = pos
            last_method_name = method
    
    if last_method_pos == -1:
        logger.error("Could not find any methods in the class")
        return False
    
    logger.info(f"Found last method: {last_method_name}")
    
    # Find the end of the last method
    # This is tricky, we'll look for the next method or the end of the file
    next_method_pos = len(content)
    for method in methods:
        if method == last_method_name:
            continue
        pos = content.find(method, last_method_pos + len(last_method_name))
        if pos != -1 and pos < next_method_pos:
            next_method_pos = pos
    
    # Insert the new methods before the last method
    new_methods = """
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
    
    def extract_key_requirements(self, job_description):
        \"\"\"Extract key requirements and keywords from job description for ATS optimization\"\"\"
        try:
            prompt = f\"\"\"
            You are an expert ATS and job requirement analyst. Extract the most important keywords, skills, 
            qualifications, and requirements from this job description that would be used by ATS systems.

            JOB DESCRIPTION:
            {job_description}

            Extract and organize the following:
            1. Required technical skills and technologies
            2. Required soft skills and qualities
            3. Required experience (years, domains, industries)
            4. Required education and certifications
            5. Key responsibilities and duties
            6. Industry-specific terminology and buzzwords
            7. Company values and culture keywords

            Format your response as a structured JSON with these categories. Include ONLY the most important 
            and frequently mentioned terms that would be critical for ATS matching.
            \"\"\"
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert ATS analyst who extracts key requirements from job descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error extracting key requirements: {str(e)}")
            return "{}"  # Return empty JSON on error
    """
    
    # Insert the new methods at the beginning of the class
    class_pos = content.find(class_def)
    if class_pos == -1:
        logger.error("Could not find class definition")
        return False
    
    # Find the end of the class definition line
    class_end = content.find("\n", class_pos) + 1
    
    # Insert the new methods after the class definition
    updated_content = content[:class_end] + new_methods + content[class_end:]
    
    # Write the updated content
    with open(service_path, 'w') as f:
        f.write(updated_content)
    
    logger.info("Successfully updated OpenAIService with new methods")
    return True

def update_resume_service():
    """Update the ResumeService class to use the new methods"""
    
    # Path to the ResumeService file
    service_path = os.path.join('app', 'services', 'resume_service.py')
    
    if not os.path.exists(service_path):
        logger.error(f"ResumeService file not found at {service_path}")
        return False
    
    # Create a backup
    if not backup_file(service_path):
        logger.error("Failed to create backup")
        return False
    
    # Read the current file
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Check if the method already exists
    if '_extract_work_experience' not in content:
        # Add helper methods to extract work experience and skills
        helper_methods = """
    def _extract_work_experience(self, user_info):
        \"\"\"Extract work experience from user info\"\"\"
        if not user_info:
            return ""
        
        # Look for work experience section
        if "Work Experience:" in user_info:
            parts = user_info.split("Work Experience:")
            if len(parts) > 1:
                # Find the next section
                next_sections = ["Education:", "Skills:", "Projects:", "Certifications:"]
                work_exp = parts[1]
                
                for section in next_sections:
                    if section in work_exp:
                        work_exp = work_exp.split(section)[0]
                
                return work_exp.strip()
        
        # If no specific section, return the whole text
        return user_info
    
    def _extract_skills(self, user_info):
        \"\"\"Extract skills from user info\"\"\"
        if not user_info:
            return ""
        
        # Look for skills section
        if "Skills:" in user_info:
            parts = user_info.split("Skills:")
            if len(parts) > 1:
                # Find the next section
                next_sections = ["Education:", "Work Experience:", "Projects:", "Certifications:"]
                skills = parts[1]
                
                for section in next_sections:
                    if section in skills:
                        skills = skills.split(section)[0]
                
                return skills.strip()
        
        # If no specific section, return empty
        return ""
        
    def _analyze_resume_vs_job(self, resume_text, job_description):
        \"\"\"Analyze how well a resume matches a job description\"\"\"
        if not resume_text or not job_description:
            return {
                "match_percentage": 0,
                "resume_word_count": 0,
                "job_word_count": 0,
                "job_keywords": [],
                "matching_keywords": []
            }
        
        # Convert to lowercase for comparison
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Count words
        resume_words = len(resume_lower.split())
        job_words = len(job_lower.split())
        
        # Extract keywords from job description
        # This is a simple approach - in production you'd use NLP
        common_words = set([
            "and", "the", "a", "an", "in", "on", "at", "to", "for", "with",
            "by", "of", "or", "as", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will", "would",
            "shall", "should", "may", "might", "must", "can", "could", "that",
            "this", "these", "those", "it", "they", "them", "their", "our", "your",
            "my", "his", "her", "its", "we", "you", "i", "he", "she"
        ])
        
        # Extract words from job description
        job_words_list = [word.strip(".,;:!?()[]{}\"'") for word in job_lower.split()]
        job_words_filtered = [word for word in job_words_list if word and word not in common_words and len(word) > 2]
        
        # Count word frequencies
        job_word_freq = {}
        for word in job_words_filtered:
            job_word_freq[word] = job_word_freq.get(word, 0) + 1
        
        # Sort by frequency
        job_keywords = sorted(job_word_freq.items(), key=lambda x: x[1], reverse=True)
        job_keywords = [word for word, freq in job_keywords[:50]]  # Top 50 keywords
        
        # Check which keywords are in the resume
        matching_keywords = []
        for keyword in job_keywords:
            if keyword in resume_lower:
                matching_keywords.append(keyword)
        
        # Calculate match percentage
        match_percentage = (len(matching_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        return {
            "match_percentage": match_percentage,
            "resume_word_count": resume_words,
            "job_word_count": job_words,
            "job_keywords": job_keywords,
            "matching_keywords": matching_keywords
        }
"""
        
        # Find a good place to insert the helper methods
        # Let's look for the end of the class
        class_def = "class ResumeService:"
        if class_def not in content:
            logger.error("ResumeService class definition not found")
            return False
        
        # Find the last method in the class
        methods = [
            "def process_resume",
            "def generate_cover_letter",
            "def generate_tailored_resume",
            "def __init__"
        ]
        
        last_method_pos = -1
        last_method_name = ""
        
        for method in methods:
            pos = content.find(method)
            if pos > last_method_pos:
                last_method_pos = pos
                last_method_name = method
        
        if last_method_pos == -1:
            logger.error("Could not find any methods in the class")
            return False
        
        logger.info(f"Found last method: {last_method_name}")
        
        # Find the end of the last method by looking for the next class or the end of the file
        next_class_pos = content.find("class ", last_method_pos + 1)
        if next_class_pos == -1:
            next_class_pos = len(content)
        
        # Insert the helper methods before the next class or end of file
        updated_content = content[:next_class_pos] + helper_methods + content[next_class_pos:]
        
        # Write the updated content
        with open(service_path, 'w') as f:
            f.write(updated_content)
        
        logger.info("Successfully updated ResumeService with helper methods")
    else:
        logger.info("Helper methods already exist in ResumeService")
    
    return True

def main():
    """Main function"""
    print("🚀 Updating OpenAI Service with ATS optimization features...")
    
    # Update OpenAIService
    if update_openai_service():
        print("✅ Successfully updated OpenAIService")
    else:
        print("❌ Failed to update OpenAIService")
        return
    
    # Update ResumeService
    if update_resume_service():
        print("✅ Successfully updated ResumeService")
    else:
        print("❌ Failed to update ResumeService")
        return
    
    print("\n🎉 Update complete! The ATS optimization features are now available.")
    print("\nTo test the new features, restart your Flask application and run:")
    print("python direct_ats_test.py")

if __name__ == "__main__":
    main()
