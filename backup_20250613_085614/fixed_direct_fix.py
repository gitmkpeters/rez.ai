#!/usr/bin/env python3
"""
Direct Fix for OpenAI Service

This script directly adds the generate_tailored_summary method to the OpenAIService class.
It makes a backup of the original file and reports success or failure.
"""

import os
import sys
import shutil
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_openai_service():
    """Add the generate_tailored_summary method to OpenAIService"""
    
    # Path to the OpenAI service file
    service_path = os.path.join('app', 'services', 'openai_service.py')
    
    if not os.path.exists(service_path):
        print(f"❌ OpenAI service file not found at {service_path}")
        return False
    
    # Create a backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{service_path}.bak_{timestamp}"
    
    try:
        shutil.copy2(service_path, backup_path)
        print(f"✅ Created backup at {backup_path}")
    except Exception as e:
        print(f"❌ Failed to create backup: {str(e)}")
        return False
    
    # Read the current file
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Check if the method already exists
    if 'def generate_tailored_summary' in content:
        print("✅ generate_tailored_summary method already exists")
        return True
    
    # Find the class definition
    class_def = "class OpenAIService:"
    if class_def not in content:
        print("❌ OpenAIService class definition not found")
        return False
    
    # Find a good insertion point - after the __init__ method
    lines = content.split('\n')
    insertion_point = None
    
    for i, line in enumerate(lines):
        if "def __init__" in line:
            # Find the end of the __init__ method
            for j in range(i+1, len(lines)):
                if lines[j].strip() == "" and j+1 < len(lines) and not lines[j+1].startswith(" "):
                    insertion_point = j + 1
                    break
            if insertion_point:
                break
    
    if insertion_point is None:
        # Fallback: insert after class definition
        for i, line in enumerate(lines):
            if class_def in line:
                insertion_point = i + 1
                break
    
    if insertion_point is None:
        print("❌ Could not find insertion point")
        return False
    
    # The new method to add - with proper indentation and escaping
    new_method = """    def generate_tailored_summary(self, work_experience, job_description, user_skills=None):
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
    
    # Insert the new method at the determined position
    lines.insert(insertion_point, new_method)
    
    # Write the updated content back to the file
    try:
        with open(service_path, 'w') as f:
            f.write('\n'.join(lines))
        print("✅ Successfully added generate_tailored_summary method to OpenAIService")
        return True
    except Exception as e:
        print(f"❌ Failed to update file: {str(e)}")
        # Restore from backup
        try:
            shutil.copy2(backup_path, service_path)
            print("✅ Restored original file from backup")
        except Exception as e2:
            print(f"❌ Failed to restore backup: {str(e2)}")
        return False

def create_simple_test():
    """Create a simple test script for the tailored summary feature"""
    test_path = "test_summary_simple.py"
    
    test_content = """#!/usr/bin/env python3
\"\"\"
Simple Test for Tailored Summary

This script tests the tailored summary generation with clear progress indicators.
\"\"\"

import os
import sys
import time
from datetime import datetime

def test_tailored_summary():
    \"\"\"Test the tailored summary generation\"\"\"
    print("\\n🚀 Testing Tailored Summary Generation\\n")
    print("=" * 60)
    
    try:
        # Import the OpenAI service
        print("⏳ Importing OpenAI service...")
        sys.stdout.flush()
        
        from app.services.openai_service import OpenAIService
        print("✅ Successfully imported OpenAIService")
        
        # Create an instance
        print("⏳ Creating OpenAI service instance...")
        sys.stdout.flush()
        
        openai_service = OpenAIService()
        print("✅ Successfully created OpenAIService instance")
        
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
        skills = "Python, JavaScript, React, Node.js, AWS, MongoDB, SQL, CI/CD, Docker, Kubernetes"
        
        # Generate tailored summary
        print("\\n⏳ Generating tailored summary (this may take 15-30 seconds)...")
        sys.stdout.flush()
        
        start_time = time.time()
        summary = openai_service.generate_tailored_summary(
            work_experience=work_experience,
            job_description=job_description,
            user_skills=skills
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ Summary generated in {elapsed_time:.2f} seconds")
        
        print("\\n✅ GENERATED TAILORED SUMMARY:\\n")
        print("-" * 60)
        print(summary)
        print("-" * 60)
        
        # Save the summary to a file
        output_dir = "ats_test_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"{output_dir}/tailored_summary_{timestamp}.txt"
        
        with open(summary_file, "w") as f:
            f.write(summary)
        
        print(f"\\n✅ Summary saved to {summary_file}")
        return True
        
    except Exception as e:
        print(f"\\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_tailored_summary()
"""
    
    try:
        with open(test_path, 'w') as f:
            f.write(test_content)
        print(f"✅ Created simple test script at {test_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Direct Fix for OpenAI Service")
    print("=" * 60)
    
    success = fix_openai_service()
    
    if success:
        print("\n✅ Successfully added the generate_tailored_summary method to OpenAIService")
        create_simple_test()
        print("\nTo test the feature, run:")
        print("python test_summary_simple.py")
    else:
        print("\n❌ Failed to update OpenAIService")
        print("Please check the error messages above.")
