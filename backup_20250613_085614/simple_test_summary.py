#!/usr/bin/env python3
"""
Simple Test for Tailored Summary

This script tests just the tailored summary generation without dependencies on other services.
"""

import os
import sys
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('summary_test')

def generate_tailored_summary(work_experience, job_description, user_skills=None):
    """Generate a highly tailored professional summary optimized for ATS and job matching"""
    try:
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY environment variable not set")
            return None
        
        client = OpenAI(api_key=api_key)
        
        # Extract key information for better targeting
        skills_text = f"\n\nKey Skills: {user_skills}" if user_skills else ""
        
        prompt = f"""
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
        """
        
        response = client.chat.completions.create(
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
        logger.info(f"Generated tailored summary: {len(summary)} characters")
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating tailored summary: {str(e)}")
        return None

def main():
    """Main function"""
    print("🚀 Testing Tailored Summary Generation")
    print("=" * 60)
    
    # Sample work experience
    work_experience = """
    Senior Software Engineer, TechCorp (2018-Present)
    - Led development of cloud-based applications using Python and AWS
    - Improved application performance by 40% through code optimization
    - Managed a team of 5 junior developers on multiple projects
    - Implemented CI/CD pipelines reducing deployment time by 60%

    Software Developer, InnovateSoft (2015-2018)
    - Developed web applications using React, Node.js, and MongoDB
    - Created RESTful APIs for mobile application backend
    - Collaborated with UX designers to implement responsive interfaces
    - Participated in Agile development process with bi-weekly sprints
    """
    
    # Sample skills
    skills = "Programming: Python, JavaScript, TypeScript, Java, SQL, HTML/CSS; Frameworks: React, Node.js, Express, Django, Flask; Tools: Git, Docker, Jenkins, AWS, Azure, Kubernetes"
    
    # Sample job description
    job_description = """
    Senior Full Stack Developer

    About Us:
    We are a leading technology company specializing in cloud-based solutions for enterprise clients. Our team is dedicated to creating innovative products that transform how businesses operate.

    Job Description:
    We are seeking an experienced Full Stack Developer to join our growing engineering team. The ideal candidate will have strong experience with Python, React, and cloud technologies. You will be responsible for developing and maintaining web applications, collaborating with cross-functional teams, and contributing to the entire software development lifecycle.

    Responsibilities:
    - Design, develop, and maintain web applications using Python and JavaScript frameworks
    - Build responsive user interfaces using React and modern frontend technologies
    - Develop RESTful APIs and backend services
    - Implement database designs and optimize queries for performance
    - Deploy and manage applications in cloud environments (AWS preferred)
    - Collaborate with product managers, designers, and other developers
    - Participate in code reviews and mentor junior developers
    - Troubleshoot and debug applications
    - Stay updated with emerging technologies and industry trends

    Requirements:
    - 5+ years of experience in software development
    - Strong proficiency in Python and JavaScript
    - Experience with React, Node.js, and modern frontend frameworks
    - Familiarity with backend frameworks like Django or Flask
    - Knowledge of database systems (SQL and NoSQL)
    - Experience with AWS or other cloud platforms
    - Understanding of CI/CD pipelines and DevOps practices
    - Excellent problem-solving and communication skills
    - Bachelor's degree in Computer Science or related field (or equivalent experience)
    """
    
    # Generate the summary
    print("Generating tailored summary...")
    summary = generate_tailored_summary(work_experience, job_description, skills)
    
    if summary:
        print("\n" + "=" * 60)
        print("GENERATED TAILORED SUMMARY:")
        print("=" * 60)
        print(summary)
        print("=" * 60 + "\n")
        
        # Save the summary to a file
        with open("tailored_summary.txt", "w") as f:
            f.write(summary)
        
        print(f"✅ Summary saved to tailored_summary.txt")
    else:
        print("❌ Failed to generate summary")

if __name__ == "__main__":
    main()
