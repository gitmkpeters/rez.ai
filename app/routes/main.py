from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
import logging
import os

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# Import resume_service with error handling
try:
    from app.services import resume_service
    if resume_service is None:
        logger.error("resume_service is None after import")
except Exception as e:
    logger.error(f"Failed to import resume_service: {str(e)}")
    resume_service = None

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@main_bp.route('/generate', methods=['GET'])
def generate():
    return render_template('generate.html')

@main_bp.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        # Check if resume_service is available
        if resume_service is None:
            flash('Resume generation service is not available. Please check your configuration.', 'error')
            return redirect(url_for('main.generate'))
        
        # Collect user information
        user_info = {
            'full_name': request.form.get('full_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'location': request.form.get('location', '').strip(),
            'linkedin': request.form.get('linkedin', '').strip(),
            'professional_summary': request.form.get('professional_summary', '').strip(),
            'work_experience': request.form.get('work_experience', '').strip(),
            'education': request.form.get('education', '').strip(),
            'skills': request.form.get('skills', '').strip(),
        }
        
        # Get job information
        job_description = request.form.get('job_description', '').strip()
        job_url = request.form.get('job_url', '').strip()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'professional_summary', 'work_experience', 'education']
        missing_fields = [field for field in required_fields if not user_info[field]]
        
        if missing_fields:
            flash(f'Please fill in required fields: {", ".join(missing_fields)}', 'error')
            return redirect(url_for('main.generate'))
        
        if not job_description and not job_url:
            flash('Please provide either a job description or a job URL', 'error')
            return redirect(url_for('main.generate'))
        
        # Format user info for AI
        formatted_user_info = f"""
        Name: {user_info['full_name']}
        Email: {user_info['email']}
        Phone: {user_info['phone']}
        Location: {user_info['location']}
        LinkedIn: {user_info['linkedin']}
        
        Professional Summary:
        {user_info['professional_summary']}
        
        Work Experience:
        {user_info['work_experience']}
        
        Education:
        {user_info['education']}
        
        Skills:
        {user_info['skills']}
        """
        
        # Generate resume using AI
        result = resume_service.generate_tailored_resume(
            user_info=formatted_user_info,
            job_description=job_description if job_description else None,
            job_url=job_url if job_url else None
        )
        
        if result["success"]:
            result["type"] = "resume"
            return render_template('generated_result.html', result=result)
        else:
            flash(result["message"], 'error')
            return redirect(url_for('main.generate'))
    
    except Exception as e:
        logger.error(f"Error in generate_resume route: {str(e)}")
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('main.generate'))

@main_bp.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        # Check if resume_service is available
        if resume_service is None:
            flash('Cover letter generation service is not available. Please check your configuration.', 'error')
            return redirect(url_for('main.generate'))
        
        # Collect user information
        user_info = {
            'full_name': request.form.get('full_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'company_name': request.form.get('company_name', '').strip(),
            'background_summary': request.form.get('background_summary', '').strip(),
            'key_achievements': request.form.get('key_achievements', '').strip(),
        }
        
        # Get job information
        job_description = request.form.get('job_description', '').strip()
        job_url = request.form.get('job_url', '').strip()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'background_summary']
        missing_fields = [field for field in required_fields if not user_info[field]]
        
        if missing_fields:
            flash(f'Please fill in required fields: {", ".join(missing_fields)}', 'error')
            return redirect(url_for('main.generate'))
        
        if not job_description and not job_url:
            flash('Please provide either a job description or a job URL', 'error')
            return redirect(url_for('main.generate'))
        
        # Format user info for AI
        formatted_user_info = f"""
        Name: {user_info['full_name']}
        Email: {user_info['email']}
        Phone: {user_info['phone']}
        
        Professional Background:
        {user_info['background_summary']}
        
        Key Achievements:
        {user_info['key_achievements']}
        """
        
        # Generate cover letter using AI
        result = resume_service.generate_cover_letter(
            user_info=formatted_user_info,
            job_description=job_description if job_description else None,
            job_url=job_url if job_url else None,
            company_name=user_info['company_name'] if user_info['company_name'] else None
        )
        
        if result["success"]:
            result["type"] = "cover letter"
            return render_template('generated_result.html', result=result)
        else:
            flash(result["message"], 'error')
            return redirect(url_for('main.generate'))
    
    except Exception as e:
        logger.error(f"Error in generate_cover_letter route: {str(e)}")
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('main.generate'))

@main_bp.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    """Analyze a generated resume for quality"""
    try:
        if resume_service is None:
            return jsonify({
                "success": False,
                "message": "Resume analysis service is not available"
            })
        
        data = request.get_json()
        resume_content = data.get('resume_content', '')
        job_description = data.get('job_description', '')
        
        if not resume_content or not job_description:
            return jsonify({
                "success": False,
                "message": "Resume content and job description are required"
            })
        
        # Analyze the resume
        result = resume_service.analyze_generated_resume(resume_content, job_description)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error analyzing resume: {str(e)}"
        })

@main_bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    """Download generated files with robust path handling - FIXED VERSION"""
    try:
        logger.info(f"Download request for file: {filename}")
        
        # List of possible directories to check (in order of preference)
        possible_paths = [
            os.path.join('app/output', filename),      # PDF files location
            os.path.join('output', filename),          # Text files location
            os.path.join('app/static/output', filename),
            os.path.join('.', filename),               # Current directory
            filename                                   # Just filename
        ]
        
        # Try each possible location
        for file_path in possible_paths:
            if os.path.exists(file_path):
                logger.info(f"✅ File found at: {file_path}")
                file_size = os.path.getsize(file_path)
                logger.info(f"File size: {file_size} bytes")
                
                # Determine the correct mimetype
                if filename.endswith('.pdf'):
                    mimetype = 'application/pdf'
                elif filename.endswith('.txt'):
                    mimetype = 'text/plain'
                else:
                    mimetype = 'application/octet-stream'
                
                logger.info(f"Serving file with mimetype: {mimetype}")
                return send_file(file_path, as_attachment=True, mimetype=mimetype)
        
        # If file not found in any location, list what files we do have
        logger.error(f"❌ File not found: {filename}")
        
        # Debug: List files in all directories
        for directory in ['output', 'app/output', 'app/static/output']:
            if os.path.exists(directory):
                files = os.listdir(directory)
                logger.info(f"Files in {directory}: {files}")
            else:
                logger.info(f"Directory {directory} does not exist")
        
        flash(f'File "{filename}" not found. It may have been moved or deleted.', 'error')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"❌ Error downloading file: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/list-files')
def list_files():
    """Debug route to list all available files"""
    try:
        file_info = {}
        directories = ['output', 'app/output', 'app/static/output']
        
        for directory in directories:
            if os.path.exists(directory):
                files = []
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        files.append({
                            'name': filename,
                            'size': size,
                            'path': file_path
                        })
                file_info[directory] = files
            else:
                file_info[directory] = "Directory does not exist"
        
        return jsonify(file_info)
        
    except Exception as e:
        return jsonify({"error": str(e)})

@main_bp.route('/process', methods=['POST'])
def process():
    try:
        if resume_service is None:
            flash('Resume processing service is not available. Please check your configuration.', 'error')
            return redirect(url_for('main.index'))
        
        # Get form data
        job_description = request.form.get('job_description', '').strip()
        job_url = request.form.get('job_url', '').strip()
        
        # Check if we have a file upload
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(url_for('main.index'))
            
        resume_file = request.files['resume']
        if resume_file.filename == '':
            flash('No resume file selected', 'error')
            return redirect(url_for('main.index'))
        
        # Validate that we have either job description or URL
        if not job_description and not job_url:
            flash('Please provide either a job description or a job URL', 'error')
            return redirect(url_for('main.index'))
        
        # Process the resume
        logger.info(f"Processing resume: {resume_file.filename}")
        logger.info(f"Job URL provided: {bool(job_url)}")
        logger.info(f"Job description provided: {len(job_description)} characters")
        
        result = resume_service.process_resume(
            resume_file=resume_file,
            job_description=job_description if job_description else None,
            job_url=job_url if job_url else None
        )
        
        if result["success"]:
            return render_template('result.html', result=result)
        else:
            # Handle URL extraction failure gracefully
            if result.get("url_error"):
                flash(result["message"], 'warning')
                return render_template('upload.html', 
                                     job_url=job_url,
                                     error_message=result["message"],
                                     url_result=result.get("url_result"))
            else:
                flash(result["message"], 'error')
                return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"Error in process route: {str(e)}")
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/test-url', methods=['POST'])
def test_url():
    """AJAX endpoint to test URL extraction"""
    try:
        if resume_service is None:
            return jsonify({"success": False, "message": "URL testing service is not available"})
        
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"success": False, "message": "No URL provided"})
        
        # Test URL extraction
        result = resume_service.process_job_url(url)
        
        return jsonify({
            "success": result["success"],
            "message": result["message"],
            "extraction_length": result.get("extraction_length", 0),
            "url_used": result.get("url_used", url),
            "job_description": result.get("job_description", "") if result["success"] else ""
        })
        
    except Exception as e:
        logger.error(f"Error testing URL: {str(e)}")
        return jsonify({"success": False, "message": f"Error testing URL: {str(e)}"})
