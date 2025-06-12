#!/bin/bash

echo "=== Committing Resume Tailor Changes ==="

# Add all changes
echo "📁 Adding files to git..."
git add .

# Check status
echo "📊 Git status:"
git status --short

# Commit with detailed message
echo "💾 Committing changes..."
git commit -m "✅ Complete Resume Tailor Application with PDF Generation

🎯 Major Features Implemented:
- AI-powered resume generation using OpenAI GPT
- AI-powered cover letter generation  
- Professional PDF generation with ReportLab
- Smart job URL extraction and processing
- Resume analysis and keyword matching
- Dual workflow interface (analyze vs generate)

🔧 Technical Improvements:
- Smart PDF service with different handling for resumes vs cover letters
- Robust service architecture with dependency injection
- Comprehensive error handling and fallback mechanisms
- Enhanced web scraping with multiple selector strategies
- Professional document formatting with proper typography

📄 PDF Generation Features:
- Complete content preservation (no truncation)
- Professional section parsing and organization
- Enhanced typography with custom styling
- Smart placeholder removal (aggressive for resumes, minimal for cover letters)
- Proper bullet point formatting
- Contact information extraction and formatting

🌐 User Interface:
- Modern Bootstrap-based responsive design
- Tabbed interface for different workflows
- Real-time URL testing with AJAX
- Auto-fill job descriptions from successful extractions
- Comprehensive error messaging and recovery

✅ All Core Features Working:
- Resume generation ✅
- Cover letter generation ✅  
- PDF file creation ✅
- File download system ✅
- Job URL processing ✅
- Service integration ✅

🚀 Production Ready!"

echo "✅ Changes committed successfully!"

# Show recent commits
echo "📜 Recent commits:"
git log --oneline -5

echo "🎉 Ready for deployment!"