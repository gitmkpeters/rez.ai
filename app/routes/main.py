import os
from flask import Blueprint, request, render_template, send_file, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename

from app.services import WebScraperService, PDFGeneratorService, OpenAIService
from app.utils.file_handlers import allowed_file, extract_text_from_file
from app.utils.validations import validate_url, validate_file_size, sanitize_filename

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize services
web_scraper = WebScraperService()

@main_bp.route("/")
def home():
    """Home page."""
    return render_template("home.html")

@main_bp.route("/upload")
def upload():
    """Upload page with form."""
    return render_template("upload.html")

@main_bp.route("/generate", methods=["POST"])
def generate():
    """Generate tailored resume."""
    try:
        # Initialize services with current app config
        pdf_service = PDFGeneratorService()
        openai_service = OpenAIService(current_app.config['OPENAI_API_KEY'])
        
        # Get and validate resume file
        resume_file = request.files.get("resume_file")
        if not resume_file or resume_file.filename == '':
            flash("Please select a resume file.", "error")
            return redirect(url_for('main.upload'))
        
        # Validate file type
        if not allowed_file(resume_file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            flash("Unsupported file type. Please upload PDF, DOCX, or TXT.", "error")
            return redirect(url_for('main.upload'))
        
        # Validate file size
        if not validate_file_size(resume_file):
            flash("File too large. Maximum size is 16MB.", "error")
            return redirect(url_for('main.upload'))
        
        # Handle job description input (text or URL)
        input_type = request.form.get("input_type", "text")
        job_description = ""
        
        if input_type == "text":
            job_description = request.form.get("job_description", "").strip()
            if not job_description:
                flash("Please provide a job description.", "error")
                return redirect(url_for('main.upload'))
        else:  # URL input
            job_url = request.form.get("job_url", "").strip()
            if not job_url:
                flash("Please provide a job URL.", "error")
                return redirect(url_for('main.upload'))
            
            if not validate_url(job_url):
                flash("Please provide a valid URL.", "error")
                return redirect(url_for('main.upload'))
            
            # Extract job description from URL
            job_description = web_scraper.extract_job_description_from_url(job_url)
            if job_description.startswith("Error") or job_description.startswith("Could not extract"):
                flash(f"URL Processing Error: {job_description}", "error")
                return redirect(url_for('main.upload'))
        
        # Save and process resume file
        filename = sanitize_filename(secure_filename(resume_file.filename))
        resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)
        
        # Extract text from resume
        resume_text = extract_text_from_file(resume_path)
        if not resume_text.strip():
            flash("Could not extract text from the resume file.", "error")
            return redirect(url_for('main.upload'))
        
        # Generate tailored resume using OpenAI
        success, result = openai_service.tailor_resume(resume_text, job_description)
        if not success:
            flash(f"Error generating tailored resume: {result}", "error")
            return redirect(url_for('main.upload'))
        
        tailored_text = result
        
        # Generate PDF
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "tailored_resume.pdf")
        pdf_success, pdf_message = pdf_service.create_resume_pdf(tailored_text, pdf_path)
        
        if not pdf_success:
            flash(f"Error creating PDF: {pdf_message}", "error")
            return redirect(url_for('main.upload'))
        
        # Clean up uploaded file
        try:
            os.remove(resume_path)
        except OSError:
            pass  # File cleanup is not critical
        
        return send_file(pdf_path, as_attachment=True, download_name="tailored_resume.pdf")
        
    except Exception as e:
        current_app.logger.error(f"Unexpected error in generate route: {str(e)}")
        flash("An unexpected error occurred. Please try again.", "error")
        return redirect(url_for('main.upload'))

@main_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html")

@main_bp.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "rez.ai"}, 200

# Error handlers for this blueprint
@main_bp.errorhandler(413)
def file_too_large(error):
    """Handle file too large error."""
    flash("File too large. Maximum size is 16MB.", "error")
    return redirect(url_for('main.upload'))

@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("errors/404.html"), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    current_app.logger.error(f"Internal error: {str(error)}")
    return render_template("errors/500.html"), 500