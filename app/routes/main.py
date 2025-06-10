# app/routes/main.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
import os
from datetime import datetime
from app.services.resume_service import ResumeService
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)
resume_service = ResumeService()

@main.context_processor
def inject_now():
    return {'now': datetime.now()}

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/upload')
def upload():
    return render_template('upload.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/generate', methods=['POST'])
def generate():
    if 'resume_file' not in request.files:
        flash('No resume file uploaded', 'error')
        return redirect(url_for('main.upload'))
    
    resume_file = request.files['resume_file']
    
    if resume_file.filename == '':
        flash('No resume file selected', 'error')
        return redirect(url_for('main.upload'))
    
    # Check file extension
    allowed_extensions = {'pdf', 'docx', 'txt'}
    if not '.' in resume_file.filename or resume_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        flash('Invalid file type. Please upload a PDF, DOCX, or TXT file', 'error')
        return redirect(url_for('main.upload'))
    
    # Get job description from form
    input_type = request.form.get('input_type', 'text')
    job_description = None
    job_url = None
    
    if input_type == 'text':
        job_description = request.form.get('job_description')
        if not job_description:
            flash('Please provide a job description', 'error')
            return redirect(url_for('main.upload'))
    else:  # input_type == 'url'
        job_url = request.form.get('job_url')
        if not job_url:
            flash('Please provide a job URL', 'error')
            return redirect(url_for('main.upload'))
    
    try:
        # Process the resume
        result = resume_service.process_resume(resume_file, job_description, job_url)
        
        # Return the PDF file
        return send_file(
            result['pdf_path'],
            as_attachment=True,
            download_name=result['filename'],
            mimetype='application/pdf'
        )
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('main.upload'))
    except Exception as e:
        current_app.logger.error(f"Error generating resume: {str(e)}")
        flash('An error occurred while processing your resume. Please try again.', 'error')
        return redirect(url_for('main.upload'))