from flask import Flask, redirect, request, session, render_template, send_file
import os
import requests
import docx
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup
import re
import html

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# LinkedIn OAuth (only if you're using it)
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
SIMULATED_MODE = os.getenv("SIMULATED_MODE", "true").lower() == "true"

# OpenAI setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filepath.endswith(".txt"):
        with open(filepath, "r") as f:
            return f.read()
    return ""

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def extract_job_description_from_url(url):
    """Extract job description from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Different extraction strategies based on the URL
        if 'linkedin.com' in url:
            job_description = extract_linkedin_job(soup)
        elif 'indeed.com' in url:
            job_description = extract_indeed_job(soup)
        elif 'glassdoor.com' in url:
            job_description = extract_glassdoor_job(soup)
        else:
            job_description = extract_generic_job(soup)
            
        if not job_description or len(job_description.strip()) < 50:
            return "Could not extract a meaningful job description from the provided URL. Please try copying and pasting the text instead."
            
        return job_description
        
    except Exception as e:
        print(f"Error extracting job description: {e}")
        return f"Error extracting job description from URL. Please try copying and pasting the text instead. Error: {str(e)}"

def extract_linkedin_job(soup):
    """Extract job description from LinkedIn."""
    # Try multiple LinkedIn selectors
    selectors = [
        'div.show-more-less-html__markup',
        'div.description__text',
        'div[class*="description"]',
        'section[class*="description"]'
    ]
    
    for selector in selectors:
        job_desc = soup.select_one(selector)
        if job_desc:
            return job_desc.get_text(separator='\n', strip=True)
    
    return None

def extract_indeed_job(soup):
    """Extract job description from Indeed."""
    selectors = [
        'div#jobDescriptionText',
        'div[data-testid="jobsearch-JobComponent-description"]',
        'div.jobsearch-jobDescriptionText'
    ]
    
    for selector in selectors:
        job_desc = soup.select_one(selector)
        if job_desc:
            return job_desc.get_text(separator='\n', strip=True)
    
    return None

def extract_glassdoor_job(soup):
    """Extract job description from Glassdoor."""
    selectors = [
        'div[data-test="job-description"]',
        'div.desc',
        'div.jobDescriptionContent'
    ]
    
    for selector in selectors:
        job_desc = soup.select_one(selector)
        if job_desc:
            return job_desc.get_text(separator='\n', strip=True)
    
    return None

def extract_generic_job(soup):
    """Generic extraction for other job sites."""
    # Try common job description containers
    selectors = [
        'div[class*="job-description" i]',
        'div[id*="job-description" i]',
        'section[class*="description" i]',
        'div[class*="description" i]',
        'div[class*="details" i]',
        'main',
        'article'
    ]
    
    for selector in selectors:
        container = soup.select_one(selector)
        if container:
            text = container.get_text(separator='\n', strip=True)
            if len(text) > 200:  # Only return if substantial content
                return text
    
    # Last resort: get all paragraph text
    paragraphs = soup.find_all('p')
    if paragraphs:
        combined_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
        if len(combined_text) > 200:
            return combined_text
        
    return None

@app.route("/generate", methods=["POST"])
def generate():
    resume_file = request.files["resume_file"]
    job_description = request.form["job_description"]
    
    if not resume_file or not job_description:
        return "Both resume and job description are required!", 400

    filename = secure_filename(resume_file.filename)
    if not allowed_file(filename):
        return "Unsupported file type. Please upload PDF, DOCX, or TXT.", 400

    # Save and extract text from resume
    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)
    resume_text = extract_text_from_file(resume_path)

    # Create prompt for OpenAI
    prompt = (
        "You're an expert career coach. Using the job description below, tailor the resume content provided "
        "to better align with the job requirements. Focus on keywords and relevance. Do not fabricate experience, "
        "but emphasize related achievements.\n\n"
        f"Job Description:\n{job_description}\n\nResume:\n{resume_text}\n\nTailored Resume:"
    )

    # Get tailored resume from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        tailored_text = response.choices[0].message.content
    except Exception as e:
        return f"Error from OpenAI: {e}", 500

    # Generate PDF using ReportLab
    pdf_path = os.path.join(UPLOAD_FOLDER, "tailored_resume.pdf")
    create_pdf_with_reportlab(tailored_text, pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name="tailored_resume.pdf")

def create_pdf_with_reportlab(text, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        if para.strip():
            # Clean up the text and handle basic formatting
            clean_para = html.unescape(para.strip())
            p = Paragraph(clean_para, styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"📄 PDF saved to {output_path}")

# LinkedIn OAuth routes (remove if not using)
@app.route("/login")
def login():
    import urllib.parse  # Only import when needed
    encoded_redirect_uri = urllib.parse.quote(REDIRECT_URI, safe='')
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&scope=r_liteprofile%20r_emailaddress%20w_member_social"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    if SIMULATED_MODE:
        session["access_token"] = "DUMMY_ACCESS_TOKEN_1234567890"
        return "Simulated access token stored."
    code = request.args.get("code")
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    token_json = response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return f"OAuth failed: {token_json}", 400
    session["access_token"] = access_token
    return "Access token stored."

if __name__ == "__main__":
    app.run(debug=True)