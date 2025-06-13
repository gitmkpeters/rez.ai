"""
Fix the duplicate app path issue and SSL problems
"""
import os
import re

def fix_pdf_service_paths():
    """Fix the duplicate app path in PDF service"""
    
    # Check if we're using the smart PDF service
    pdf_service_file = "app/services/smart_pdf_service.py"
    
    if os.path.exists(pdf_service_file):
        print("🔧 Fixing PDF service paths...")
        
        with open(pdf_service_file, 'r') as f:
            content = f.read()
        
        # Fix the default output_dir parameter to avoid duplicate app
        content = content.replace(
            'output_dir="app/output"',
            'output_dir="output"'
        )
        
        with open(pdf_service_file, 'w') as f:
            f.write(content)
        
        print("✅ Fixed PDF service paths")
    
    # Also check the main PDF service
    main_pdf_service = "app/services/pdf_service.py"
    if os.path.exists(main_pdf_service):
        print("🔧 Fixing main PDF service paths...")
        
        with open(main_pdf_service, 'r') as f:
            content = f.read()
        
        content = content.replace(
            'output_dir="app/output"',
            'output_dir="output"'
        )
        
        with open(main_pdf_service, 'w') as f:
            f.write(content)
        
        print("✅ Fixed main PDF service paths")

def fix_resume_service_paths():
    """Fix paths in resume service"""
    
    resume_service_file = "app/services/resume_service.py"
    
    if os.path.exists(resume_service_file):
        print("🔧 Fixing resume service paths...")
        
        with open(resume_service_file, 'r') as f:
            content = f.read()
        
        # Fix any hardcoded app/output paths
        content = re.sub(
            r'output_dir\s*=\s*["\']app/output["\']',
            'output_dir="output"',
            content
        )
        
        with open(resume_service_file, 'w') as f:
            f.write(content)
        
        print("✅ Fixed resume service paths")

def create_output_directory():
    """Ensure the correct output directory exists"""
    
    directories = ["output", "app/output"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def debug_current_paths():
    """Debug current path configuration"""
    
    print("\n🔍 DEBUGGING CURRENT PATHS:")
    print("=" * 40)
    
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if directories exist
    directories = ["output", "app/output", "app/app/output"]
    
    for directory in directories:
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"✅ {directory}: {len(files)} files")
            for file in files[:3]:  # Show first 3 files
                print(f"   - {file}")
        else:
            print(f"❌ {directory}: Does not exist")

if __name__ == "__main__":
    print("🔧 Fixing Path and SSL Issues")
    print("=" * 40)
    
    # Debug current state
    debug_current_paths()
    
    # Fix the path issues
    fix_pdf_service_paths()
    fix_resume_service_paths()
    create_output_directory()
    
    # Debug after fixes
    print("\n🔍 AFTER FIXES:")
    debug_current_paths()
    
    print("\n✅ Path fixes complete!")
    print("\nNext steps:")
    print("1. Restart your Flask app")
    print("2. Access via: http://localhost:5000 (HTTP only)")
    print("3. Generate a test resume")
