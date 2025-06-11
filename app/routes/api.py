from flask import Blueprint, request, jsonify, current_app
from app.services import JobScraper, OpenAIService
from app.utils.validators import validate_url

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
web_scraper = JobScraper()

@api_bp.route("/extract-job", methods=["POST"])
def extract_job_description():
    """API endpoint to extract job description from URL."""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url'].strip()
        
        if not validate_url(url):
            return jsonify({"error": "Invalid URL format"}), 400
        
        job_description = web_scraper.extract_job_description_from_url(url)
        
        if job_description.startswith("Error") or job_description.startswith("Could not extract"):
            return jsonify({"error": job_description}), 400
        
        return jsonify({
            "success": True,
            "job_description": job_description,
            "url": url
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in extract_job_description: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route("/tailor-resume", methods=["POST"])
def tailor_resume_api():
    """API endpoint for resume tailoring."""
    try:
        data = request.get_json()
        
        required_fields = ['resume_text', 'job_description']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "resume_text and job_description are required"}), 400
        
        openai_service = OpenAIService(current_app.config['OPENAI_API_KEY'])
        
        success, result = openai_service.tailor_resume(
            data['resume_text'], 
            data['job_description'],
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 1000)
        )
        
        if not success:
            return jsonify({"error": result}), 500
        
        return jsonify({
            "success": True,
            "tailored_resume": result
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in tailor_resume_api: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route("/health", methods=["GET"])
def api_health():
    """API health check."""
    return jsonify({
        "status": "healthy",
        "service": "rez.ai API",
        "version": "1.0.0"
    })