#!/usr/bin/env python3
"""
Rollback Script - Restore to Working State
==========================================
This script restores the application to the working state before template issues.
"""

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_file(file_path, content):
    """Create a file with the given content"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"✅ Restored: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to restore {file_path}: {str(e)}")
        return False

def main():
    print("🔄 Rolling back to working state...")
    print("=" * 50)
    
    # Restore original upload.html with working analyze/generate functionality
    upload_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resume Tailor - Upload Job & Resume</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<style>
    body {
        padding: 20px;
        background-color: #f8f9fa;
    }
    .container {
        max-width: 800px;
    }
    .card {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .form-group label {
        font-weight: 600;
    }
    .url-test-result {
        margin-top: 10px;
        padding: 10px;
        border-radius: 5px;
        display: none;
    }
    .url-test-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .url-test-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .loading {
        display: none;
    }
    .btn-test-url {
        margin-top: 5px;
    }
    .workflow-options {
        background-color: #e9ecef;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    .nav-bar {
        background-color: #fff;
        padding: 10px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #dee2e6;
    }
    .nav-links {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-links a {
        text-decoration: none;
        color: #495057;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    .nav-links a:hover {
        background-color: #e9ecef;
        text-decoration: none;
        color: #495057;
    }
    .nav-links .active {
        background-color: #007bff;
        color: white;
    }
</style>
</head>
<body>

<!-- Navigation -->
<div class="nav-bar">
    <div class="container">
        <div class="nav-links">
            <a href="/" class="h4 mb-0">Resume Tailor</a>
            <div>
                <a href="/" class="active">Home</a>
                <a href="/generate">Generate</a>
                <a href="/profile">Profile</a>
            </div>
        </div>
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-12">
            <!-- Workflow Options -->
            <div class="workflow-options">
                <h3>Choose Your Workflow</h3>
                <p class="text-muted">Analyze an existing resume or generate new documents with AI</p>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <h5>📊 Analyze Existing Resume</h5>
                                <p>Upload your current resume and see how it matches a job description</p>
                                <button class="btn btn-primary" onclick="showAnalysisForm()">Analyze Resume</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <h5>🤖 Generate with AI</h5>
                                <p>Create tailored resumes and cover letters using artificial intelligence</p>
                                <a href="/generate" class="btn btn-success">Generate Documents</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Analysis Form (hidden by default) -->
            <div class="card" id="analysis-form" style="display: none;">
                <div class="card-header">
                    <h2 class="mb-0">Resume Analysis</h2>
                    <p class="mb-0 text-muted">Upload your resume and provide a job description to get tailored suggestions</p>
                </div>
                <div class="card-body">
                    <!-- Flash messages -->
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ 'danger' if category == 'error' else 'warning' if category == 'warning' else 'info' }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}

                    <!-- URL Error Message -->
                    {% if error_message %}
                    <div class="alert alert-warning">
                        <strong>URL Extraction Failed:</strong> {{ error_message }}
                        <p class="mt-2 mb-0">Please copy and paste the job description below:</p>
                    </div>
                    {% endif %}

                    <form action="{{ url_for('main.process') }}" method="post" enctype="multipart/form-data">
                        <!-- Resume Upload -->
                        <div class="form-group">
                            <label for="resume">Resume File *</label>
                            <input type="file" name="resume" id="resume" class="form-control-file" 
                                   accept=".pdf,.doc,.docx" required>
                            <small class="form-text text-muted">Supported formats: PDF, DOC, DOCX</small>
                        </div>

                        <!-- Job URL -->
                        <div class="form-group">
                            <label for="job_url">Job URL (Optional)</label>
                            <input type="url" name="job_url" id="job_url" class="form-control" 
                                   placeholder="https://www.linkedin.com/jobs/view/1234567890" 
                                   value="{{ job_url or '' }}">
                            <button type="button" class="btn btn-sm btn-outline-primary btn-test-url" onclick="testUrl()">
                                Test URL
                            </button>
                            <div class="loading">
                                <small class="text-muted">Testing URL...</small>
                            </div>
                            <div class="url-test-result" id="url-test-result"></div>
                            <small class="form-text text-muted">
                                Paste a LinkedIn job URL here. We'll try to extract the job description automatically.
                            </small>
                        </div>

                        <!-- Job Description -->
                        <div class="form-group">
                            <label for="job_description">Job Description {{ '(Required if no URL provided)' if not job_url else '(Optional if URL works)' }}</label>
                            <textarea name="job_description" id="job_description" class="form-control" rows="8" 
                                      placeholder="Paste the job description here...">{{ request.form.get('job_description', '') }}</textarea>
                            <small class="form-text text-muted">
                                Copy and paste the full job description from the job posting.
                            </small>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg btn-block">
                            📊 Analyze Resume
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

<script>
    function showAnalysisForm() {
        document.querySelector('.workflow-options').style.display = 'none';
        document.getElementById('analysis-form').style.display = 'block';
    }

    function testUrl() {
        const urlInput = document.getElementById('job_url');
        const url = urlInput.value.trim();
        const resultDiv = document.getElementById('url-test-result');
        const loadingDiv = document.querySelector('.loading');
        
        if (!url) {
            alert('Please enter a URL first');
            return;
        }
        
        // Show loading
        loadingDiv.style.display = 'block';
        resultDiv.style.display = 'none';
        
        // Test the URL
        fetch('/test-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            
            if (data.success) {
                resultDiv.className = 'url-test-result url-test-success';
                resultDiv.innerHTML = `
                    <strong>✅ Success!</strong> ${data.message}<br>
                    <small>Extracted ${data.extraction_length} characters from job posting</small>
                `;
            } else {
                resultDiv.className = 'url-test-result url-test-error';
                resultDiv.innerHTML = `
                    <strong>❌ Failed:</strong> ${data.message}
                `;
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.className = 'url-test-result url-test-error';
            resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
        });
    }
</script>
</body>
</html>'''

    # Restore base.html template for profile system
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Resume Tailor{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .nav-bar {
            background-color: #fff;
            padding: 10px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid #dee2e6;
        }
        .nav-links {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .nav-links a {
            text-decoration: none;
            color: #495057;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        .nav-links a:hover {
            background-color: #e9ecef;
            text-decoration: none;
            color: #495057;
        }
        .nav-links .active {
            background-color: #007bff;
            color: white;
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <div class="nav-bar">
        <div class="nav-links">
            <a href="/" class="text-xl font-bold">Resume Tailor</a>
            <div class="space-x-2">
                <a href="/">Home</a>
                <a href="/generate">Generate</a>
                <a href="/profile">Profile</a>
            </div>
        </div>
    </div>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
                {% for category, message in messages %}
                    <div class="alert mb-4 p-4 rounded-lg {% if category == 'error' %}bg-red-100 text-red-700 border border-red-300{% else %}bg-green-100 text-green-700 border border-green-300{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t mt-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <p class="text-center text-gray-500">&copy; 2025 Resume Tailor. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''

    # Files to restore
    files_to_restore = [
        ('app/templates/upload.html', upload_html),
        ('app/templates/base.html', base_html),
    ]
    
    success_count = 0
    for file_path, content in files_to_restore:
        if create_file(file_path, content):
            success_count += 1
    
    print(f"\n🎉 Rollback complete!")
    print(f"✅ Restored {success_count}/{len(files_to_restore)} files")
    print("\nNext steps:")
    print("1. Restart your Flask app: python run_http_only.py")
    print("2. Test the main page functionality")
    print("3. Test the profile system")

if __name__ == "__main__":
    main()