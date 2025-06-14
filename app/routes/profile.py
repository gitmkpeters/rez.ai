"""
Profile Routes

This module defines the routes for user profile management.
"""

import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.services.profile_service import ProfileService
from app.db.schema import initialize_database

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
logger = logging.getLogger(__name__)

# Initialize the database when the blueprint is registered
@profile_bp.record_once
def on_load(state):
    initialize_database()
    logger.info("Profile database initialized")

# Initialize service
profile_service = ProfileService()

@profile_bp.route('/', methods=['GET'])
def profile_home():
    """Profile management home page"""
    # Get user ID from session or use a default for demo
    user_id = session.get('user_id', request.args.get('user_id', 'demo@example.com'))
    
    # Get profile if it exists
    profile = profile_service.get_profile_by_user_id(user_id)
    
    return render_template('profile/index.html', profile=profile, user_id=user_id)

@profile_bp.route('/test', methods=['GET'])
def profile_test():
    """Test route to verify profile blueprint is working"""
    return jsonify({
        'status': 'success',
        'message': 'Profile blueprint is working!',
        'blueprint': 'profile_bp'
    })

@profile_bp.route('/edit', methods=['GET'])
def edit_profile():
    """Edit profile page"""
    # Get user ID from session or use a default for demo
    user_id = session.get('user_id', request.args.get('user_id', 'demo@example.com'))
    
    # Get profile if it exists
    profile = profile_service.get_profile_by_user_id(user_id)
    
    return render_template('profile/edit.html', profile=profile, user_id=user_id)

@profile_bp.route('/save', methods=['POST'])
def save_profile():
    """Save profile data"""
    try:
        # Get user ID from session or form
        user_id = session.get('user_id', request.form.get('user_id', 'demo@example.com'))
        
        # Collect basic profile data
        profile_data = {
            'user_id': user_id,
            'full_name': request.form.get('full_name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'location': request.form.get('location', ''),
            'linkedin': request.form.get('linkedin', ''),
            'website': request.form.get('website', ''),
            'summary': request.form.get('summary', '')
        }
        
        # Create or update profile
        profile = profile_service.create_or_update_profile(profile_data)
        
        if profile:
            flash('Profile saved successfully!', 'success')
            return redirect(url_for('profile.profile_home', user_id=user_id))
        else:
            flash('Failed to save profile. Please try again.', 'error')
            return redirect(url_for('profile.edit_profile', user_id=user_id))
    
    except Exception as e:
        logger.error(f"Error saving profile: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('profile.edit_profile'))

@profile_bp.route('/work-experience/add', methods=['GET', 'POST'])
def add_work_experience():
    """Add work experience"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    if request.method == 'POST':
        try:
            # Get profile
            profile = profile_service.get_profile_by_user_id(user_id)
            if not profile:
                flash('Profile not found. Please create a profile first.', 'error')
                return redirect(url_for('profile.edit_profile', user_id=user_id))
            
            # Collect work experience data
            experience_data = {
                'company': request.form.get('company', ''),
                'position': request.form.get('position', ''),
                'start_date': request.form.get('start_date', ''),
                'end_date': request.form.get('end_date', ''),
                'is_current': 'is_current' in request.form,
                'description': request.form.get('description', ''),
                'achievements': request.form.get('achievements', '')
            }
            
            # Add work experience
            experience_id = profile_service.add_work_experience(profile.id, experience_data)
            
            if experience_id:
                flash('Work experience added successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to add work experience. Please try again.', 'error')
                return render_template('profile/work_experience_form.html', user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error adding work experience: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/work_experience_form.html', user_id=user_id)
    
    return render_template('profile/work_experience_form.html', user_id=user_id)

@profile_bp.route('/work-experience/edit/<int:experience_id>', methods=['GET', 'POST'])
def edit_work_experience(experience_id):
    """Edit work experience"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    # Get profile
    profile = profile_service.get_profile_by_user_id(user_id)
    if not profile:
        flash('Profile not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    # Find the work experience
    experience = next((exp for exp in profile.work_experiences if exp.id == experience_id), None)
    if not experience:
        flash('Work experience not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    if request.method == 'POST':
        try:
            # Collect work experience data
            experience_data = {
                'profile_id': profile.id,
                'company': request.form.get('company', ''),
                'position': request.form.get('position', ''),
                'start_date': request.form.get('start_date', ''),
                'end_date': request.form.get('end_date', ''),
                'is_current': 'is_current' in request.form,
                'description': request.form.get('description', ''),
                'achievements': request.form.get('achievements', '')
            }
            
            # Update work experience
            success = profile_service.update_work_experience(experience_id, experience_data)
            
            if success:
                flash('Work experience updated successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to update work experience. Please try again.', 'error')
                return render_template('profile/work_experience_form.html', experience=experience, user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error updating work experience: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/work_experience_form.html', experience=experience, user_id=user_id)
    
    return render_template('profile/work_experience_form.html', experience=experience, user_id=user_id)

@profile_bp.route('/work-experience/delete/<int:experience_id>', methods=['POST'])
def delete_work_experience(experience_id):
    """Delete work experience"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.form.get('user_id', 'demo@example.com'))
    
    try:
        # Delete work experience
        success = profile_service.delete_work_experience(experience_id)
        
        if success:
            flash('Work experience deleted successfully!', 'success')
        else:
            flash('Failed to delete work experience.', 'error')
    
    except Exception as e:
        logger.error(f"Error deleting work experience: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('profile.profile_home', user_id=user_id))

@profile_bp.route('/education/add', methods=['GET', 'POST'])
def add_education():
    """Add education"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    if request.method == 'POST':
        try:
            # Get profile
            profile = profile_service.get_profile_by_user_id(user_id)
            if not profile:
                flash('Profile not found. Please create a profile first.', 'error')
                return redirect(url_for('profile.edit_profile', user_id=user_id))
            
            # Collect education data
            education_data = {
                'institution': request.form.get('institution', ''),
                'degree': request.form.get('degree', ''),
                'field_of_study': request.form.get('field_of_study', ''),
                'start_date': request.form.get('start_date', ''),
                'end_date': request.form.get('end_date', ''),
                'is_current': 'is_current' in request.form,
                'description': request.form.get('description', '')
            }
            
            # Add education
            education_id = profile_service.add_education(profile.id, education_data)
            
            if education_id:
                flash('Education added successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to add education. Please try again.', 'error')
                return render_template('profile/education_form.html', user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error adding education: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/education_form.html', user_id=user_id)
    
    return render_template('profile/education_form.html', user_id=user_id)

@profile_bp.route('/education/edit/<int:education_id>', methods=['GET', 'POST'])
def edit_education(education_id):
    """Edit education"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    # Get profile
    profile = profile_service.get_profile_by_user_id(user_id)
    if not profile:
        flash('Profile not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    # Find the education
    education = next((edu for edu in profile.education if edu.id == education_id), None)
    if not education:
        flash('Education not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    if request.method == 'POST':
        try:
            # Collect education data
            education_data = {
                'profile_id': profile.id,
                'institution': request.form.get('institution', ''),
                'degree': request.form.get('degree', ''),
                'field_of_study': request.form.get('field_of_study', ''),
                'start_date': request.form.get('start_date', ''),
                'end_date': request.form.get('end_date', ''),
                'is_current': 'is_current' in request.form,
                'description': request.form.get('description', '')
            }
            
            # Update education
            success = profile_service.update_education(education_id, education_data)
            
            if success:
                flash('Education updated successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to update education. Please try again.', 'error')
                return render_template('profile/education_form.html', education=education, user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error updating education: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/education_form.html', education=education, user_id=user_id)
    
    return render_template('profile/education_form.html', education=education, user_id=user_id)

@profile_bp.route('/education/delete/<int:education_id>', methods=['POST'])
def delete_education(education_id):
    """Delete education"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.form.get('user_id', 'demo@example.com'))
    
    try:
        # Delete education
        success = profile_service.delete_education(education_id)
        
        if success:
            flash('Education deleted successfully!', 'success')
        else:
            flash('Failed to delete education.', 'error')
    
    except Exception as e:
        logger.error(f"Error deleting education: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('profile.profile_home', user_id=user_id))

@profile_bp.route('/skill/add', methods=['GET', 'POST'])
def add_skill():
    """Add skill"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    if request.method == 'POST':
        try:
            # Get profile
            profile = profile_service.get_profile_by_user_id(user_id)
            if not profile:
                flash('Profile not found. Please create a profile first.', 'error')
                return redirect(url_for('profile.edit_profile', user_id=user_id))
            
            # Collect skill data
            skill_data = {
                'name': request.form.get('name', ''),
                'level': request.form.get('level', ''),
                'category': request.form.get('category', '')
            }
            
            # Add skill
            skill_id = profile_service.add_skill(profile.id, skill_data)
            
            if skill_id:
                flash('Skill added successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to add skill. Please try again.', 'error')
                return render_template('profile/skill_form.html', user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/skill_form.html', user_id=user_id)
    
    return render_template('profile/skill_form.html', user_id=user_id)

@profile_bp.route('/skill/edit/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    """Edit skill"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.args.get('user_id', request.form.get('user_id', 'demo@example.com')))
    
    # Get profile
    profile = profile_service.get_profile_by_user_id(user_id)
    if not profile:
        flash('Profile not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    # Find the skill
    skill = next((s for s in profile.skills if s.id == skill_id), None)
    if not skill:
        flash('Skill not found.', 'error')
        return redirect(url_for('profile.profile_home', user_id=user_id))
    
    if request.method == 'POST':
        try:
            # Collect skill data
            skill_data = {
                'profile_id': profile.id,
                'name': request.form.get('name', ''),
                'level': request.form.get('level', ''),
                'category': request.form.get('category', '')
            }
            
            # Update skill
            success = profile_service.update_skill(skill_id, skill_data)
            
            if success:
                flash('Skill updated successfully!', 'success')
                return redirect(url_for('profile.profile_home', user_id=user_id))
            else:
                flash('Failed to update skill. Please try again.', 'error')
                return render_template('profile/skill_form.html', skill=skill, user_id=user_id)
        
        except Exception as e:
            logger.error(f"Error updating skill: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile/skill_form.html', skill=skill, user_id=user_id)
    
    return render_template('profile/skill_form.html', skill=skill, user_id=user_id)

@profile_bp.route('/skill/delete/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    """Delete skill"""
    # Get user ID from session or request
    user_id = session.get('user_id', request.form.get('user_id', 'demo@example.com'))
    
    try:
        # Delete skill
        success = profile_service.delete_skill(skill_id)
        
        if success:
            flash('Skill deleted successfully!', 'success')
        else:
            flash('Failed to delete skill.', 'error')
    
    except Exception as e:
        logger.error(f"Error deleting skill: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('profile.profile_home', user_id=user_id))

# API endpoints for AJAX requests
@profile_bp.route('/api/profile/<user_id>', methods=['GET'])
def get_profile_api(user_id):
    """Get profile data as JSON"""
    try:
        profile = profile_service.get_profile_by_user_id(user_id)
        
        if profile:
            # Convert profile to dictionary
            profile_dict = {
                'id': profile.id,
                'user_id': profile.user_id,
                'full_name': profile.full_name,
                'email': profile.email,
                'phone': profile.phone,
                'location': profile.location,
                'linkedin': profile.linkedin,
                'website': profile.website,
                'summary': profile.summary,
                'work_experiences': [
                    {
                        'id': exp.id,
                        'company': exp.company,
                        'position': exp.position,
                        'start_date': exp.start_date,
                        'end_date': exp.end_date,
                        'is_current': exp.is_current,
                        'description': exp.description,
                        'achievements': exp.achievements
                    } for exp in profile.work_experiences
                ],
                'education': [
                    {
                        'id': edu.id,
                        'institution': edu.institution,
                        'degree': edu.degree,
                        'field_of_study': edu.field_of_study,
                        'start_date': edu.start_date,
                        'end_date': edu.end_date,
                        'is_current': edu.is_current,
                        'description': edu.description
                    } for edu in profile.education
                ],
                'certifications': [
                    {
                        'id': cert.id,
                        'name': cert.name,
                        'issuing_organization': cert.issuing_organization,
                        'issue_date': cert.issue_date,
                        'expiration_date': cert.expiration_date,
                        'credential_id': cert.credential_id,
                        'credential_url': cert.credential_url
                    } for cert in profile.certifications
                ],
                'skills': [
                    {
                        'id': skill.id,
                        'name': skill.name,
                        'level': skill.level,
                        'category': skill.category
                    } for skill in profile.skills
                ]
            }
            
            return jsonify({'success': True, 'profile': profile_dict})
        else:
            return jsonify({'success': False, 'message': 'Profile not found'})
    
    except Exception as e:
        logger.error(f"Error getting profile API: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@profile_bp.route('/api/profile', methods=['POST'])
def save_profile_api():
    """Save profile data via API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # Create or update profile
        profile = profile_service.create_or_update_profile(data)
        
        if profile:
            return jsonify({'success': True, 'message': 'Profile saved successfully', 'profile_id': profile.id})
        else:
            return jsonify({'success': False, 'message': 'Failed to save profile'})
    
    except Exception as e:
        logger.error(f"Error saving profile API: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})
