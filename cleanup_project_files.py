"""
Clean up temporary and debug files from the project
"""
import os
import shutil
import glob

def cleanup_files():
    """Remove temporary, debug, and backup files"""
    
    print("=== Cleaning Up Project Files ===")
    
    # Files and patterns to remove
    cleanup_patterns = [
        # Debug and test files
        "debug_*.py",
        "test_*.py",
        "fix_*.py",
        "update_*.py",
        "check_*.py",
        "setup_*.py",
        "verify_*.py",
        "force_*.py",
        
        # Backup files
        "*.backup*",
        "app/services/*.backup*",
        
        # Temporary files
        "temp_*",
        "*.tmp",
        
        # Output test files (keep the directory structure)
        "output/Test_*",
        "output/Mike_Peterson_*",
        "app/output/Test_*",
        "app/output/Mike_Peterson_*",
        
        # HTML debug files
        "debug_html/*",
        
        # Specific files we created during debugging
        "run_app.py",
        "run.py",
        "test_simple_pdf.py",
        "test_simple_output.py",
        "app/services/simple_pdf_service.py.backup",
        "app/services/fallback_resume_service.py",
        "app/services/working_pdf_service.py",
        "app/services/improved_pdf_service.py",
        "app/services/enhanced_pdf_service.py",
        "app/services/smart_pdf_service.py",
        "app/routes/main_fixed.py"
    ]
    
    removed_files = []
    kept_files = []
    
    # Remove files matching patterns
    for pattern in cleanup_patterns:
        matches = glob.glob(pattern, recursive=True)
        for file_path in matches:
            if os.path.exists(file_path):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_files.append(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        removed_files.append(file_path + "/")
                except Exception as e:
                    print(f"⚠️ Could not remove {file_path}: {str(e)}")
                    kept_files.append(file_path)
    
    # Clean up empty directories
    empty_dirs = ["debug_html"]
    for dir_path in empty_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            try:
                if not os.listdir(dir_path):  # Directory is empty
                    os.rmdir(dir_path)
                    removed_files.append(dir_path + "/")
            except Exception as e:
                print(f"⚠️ Could not remove directory {dir_path}: {str(e)}")
    
    # Report results
    print(f"\n✅ Cleanup completed!")
    print(f"📁 Removed {len(removed_files)} files/directories")
    
    if removed_files:
        print("\nRemoved files:")
        for file_path in sorted(removed_files):
            print(f"  - {file_path}")
    
    if kept_files:
        print(f"\n⚠️ Could not remove {len(kept_files)} files:")
        for file_path in kept_files:
            print(f"  - {file_path}")
    
    return len(removed_files), len(kept_files)

def list_remaining_files():
    """List the core project files that remain"""
    print("\n=== Core Project Files ===")
    
    core_files = [
        "app/__init__.py",
        "app/routes/__init__.py",
        "app/routes/main.py",
        "app/services/__init__.py",
        "app/services/scraper.py",
        "app/services/document_service.py",
        "app/services/openai_service.py",
        "app/services/pdf_service.py",
        "app/services/resume_service.py",
        "app/templates/upload.html",
        "app/templates/generate.html",
        "app/templates/result.html",
        "app/templates/generated_result.html",
        "requirements.txt",
        "run_simple.py",
        ".env",
        "CHANGELOG.md"
    ]
    
    print("\nCore application files:")
    for file_path in core_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} (missing)")
    
    # Check output directories
    print("\nOutput directories:")
    output_dirs = ["output", "app/output", "uploads", "app/uploads"]
    for dir_path in output_dirs:
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            print(f"  📁 {dir_path}/ ({len(files)} files)")
        else:
            print(f"  📁 {dir_path}/ (does not exist)")

if __name__ == "__main__":
    removed_count, kept_count = cleanup_files()
    list_remaining_files()
    
    print(f"\n🎉 Project cleanup completed!")
    print(f"✅ Removed: {removed_count} files")
    print(f"⚠️ Kept: {kept_count} files")
    print("\nReady for commit! 🚀")