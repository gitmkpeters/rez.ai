from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services import resume_service
import logging
import os

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/test-env', methods=['GET'])
def test_env():
    """Test route to check if environment variables are loaded"""
    api_key = os.getenv('OPENAI_API_KEY')
    return jsonify({
        'api_key_exists': bool(api_key),
        'api_key_length': len(api_key) if api_key else 0,
        'api_key_prefix': api_key[:10] + '...' if api_key else 'None'
    })

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@main_bp.route('/generate', methods=['GET'])
def generate():
    return render_template('generate.html')

@main_bp.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
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

@main_bp.route('/process', methods=['POST'])
def process():
    try:
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
