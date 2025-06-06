from flask import Flask, redirect, request, session, url_for, render_template, send_file
import os
import requests
import urllib.parse
import docx
import re
from collections import Counter
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

# Allowed resume file types
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Environment config
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
SIMULATED_MODE = os.getenv("SIMULATED_MODE", "true").lower() == "true"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    encoded_redirect_uri = urllib.parse.quote(REDIRECT_URI, safe='')
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&scope=r_liteprofile%20r_emailaddress%20w_member_social"
    )
    print(f"[{'SIM' if SIMULATED_MODE else 'LIVE'}] Redirecting to LinkedIn: {auth_url}")
    return redirect(auth_url)

@app.route("/callback")
def callback():
    if SIMULATED_MODE:
        access_token = "DUMMY_ACCESS_TOKEN_1234567890"
        session["access_token"] = access_token
        return f"Simulated access token stored: {access_token[:12]}..."
    else:
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
            return f"OAuth failed. Response: {token_json}", 400

        session["access_token"] = access_token
        return f"Access token: {access_token[:12]}... stored in session"

@app.route("/profile")
def profile():
    access_token = session.get("access_token")
    if not access_token:
        return "You must log in with LinkedIn first.", 401

    if SIMULATED_MODE:
        profile_data = {
            "localizedFirstName": "Mike",
            "localizedLastName": "Peterson",
            "headline": "Developer • AI Builder • Database Expert",
            "emailAddress": "jprflipside@gmail.com"
        }
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_resp = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        email_resp = requests.get(
            "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
            headers=headers
        )
        profile_data = profile_resp.json()
        email_data = email_resp.json()

        profile_data = {
            "localizedFirstName": profile_data.get("localizedFirstName", ""),
            "localizedLastName": profile_data.get("localizedLastName", ""),
            "headline": profile_data.get("headline", {}).get("localized", {}).get("en_US", ""),
            "emailAddress": email_data.get("elements", [{}])[0].get("handle~", {}).get("emailAddress", "")
        }

    return (
        f"<h2>LinkedIn Profile ({'Simulated' if SIMULATED_MODE else 'Live'})</h2>"
        f"<p><strong>Name:</strong> {profile_data['localizedFirstName']} {profile_data['localizedLastName']}</p>"
        f"<p><strong>Headline:</strong> {profile_data['headline']}</p>"
        f"<p><strong>Email:</strong> {profile_data['emailAddress']}</p>"
    )

@app.route("/post")
def post_to_linkedin():
    access_token = session.get("access_token")
    if not access_token:
        return "You must log in with LinkedIn first.", 401

    if SIMULATED_MODE:
        post_data = {
            "author": "urn:li:person:1234567890",
            "text": "Testing post from rez.ai — automation is coming!"
        }
        print("✅ [Simulated Post]")
        print(post_data)
        return "✅ Simulated post created successfully!"
    else:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        # Replace with dynamic user ID in production
        author_urn = "urn:li:person:YOUR_REAL_LINKEDIN_ID"

        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": "Testing post from rez.ai — automation is coming!"},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_data)
        if response.status_code != 201:
            return f"❌ Post failed: {response.status_code} - {response.text}", 400

        return "✅ Real LinkedIn post submitted!"

@app.route("/upload")
def upload():
    return render_template("upload.html")

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

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

def match_keywords(job_description, resume_text, top_n=10):
    job_words = re.findall(r'\b\w+\b', job_description.lower())
    resume_words = re.findall(r'\b\w+\b', resume_text.lower())
    stopwords = {"and", "or", "the", "with", "a", "to", "in", "of", "on", "for", "at", "as", "by", "an", "is"}
    job_keywords = [word for word in job_words if word not in stopwords and len(word) > 2]
    top_keywords = [kw for kw, _ in Counter(job_keywords).most_common(top_n)]
    matched_keywords = [kw for kw in top_keywords if kw in resume_words]
    return matched_keywords, top_keywords

@app.route("/generate", methods=["POST"])
def generate():
    resume_file = request.files["resume_file"]
    job_description = request.form["job_description"]

    if not resume_file or not job_description:
        return "Both resume and job description are required!", 400

    filename = secure_filename(resume_file.filename)
    if not allowed_file(filename):
        return "Unsupported file type. Please upload a PDF, DOCX, or TXT file.", 400

    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)

    resume_text = extract_text_from_file(resume_path)
    matched_keywords, top_keywords = match_keywords(job_description, resume_text)

    tailored_resume_path = os.path.join(UPLOAD_FOLDER, "tailored_resume.txt")
    with open(tailored_resume_path, "w") as f:
        f.write("Simulated Tailored Resume\n")
        f.write("=========================\n")
        f.write(f"\n[Top Job Description Keywords]:\n{', '.join(top_keywords)}\n")
        f.write(f"\n[Matched Resume Keywords]:\n{', '.join(matched_keywords)}\n")
        f.write("\n[Extracted Resume Sample]:\n")
        f.write(resume_text[:500])

    return send_file(tailored_resume_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)