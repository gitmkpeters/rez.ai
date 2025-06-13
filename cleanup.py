#!/usr/bin/env python3
"""
Project Cleanup Script

This script cleans up unnecessary files from the project directory.
"""

import os
import shutil
from datetime import datetime
import re

def backup_directory(name="backup"):
    """Create a backup directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{name}_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

def cleanup_project():
    """Clean up unnecessary files from the project directory"""
    print("🧹 Starting project cleanup...")
    
    # Create backup directory
    backup_dir = backup_directory()
    print(f"📁 Created backup directory: {backup_dir}")
    
    # Files to move to backup (instead of deleting directly)
    files_to_backup = [
        # Backup files
        "app/services/openai_service.py.20250612_164356.bak",
        "app/services/openai_service.py.20250612_164925.bak",
        "app/services/openai_service.py.bak_20250612_183751",
        "app/services/resume_service.py.20250612_164356.bak",
        "app/services/resume_service.py.20250612_164925.bak",
        
        # Temporary fix scripts
        "direct_fix.py",
        "direct_fix_openai_service.py",
        "fix_download_path.py",
        "fix_filepath_issue.py",
        "fix_ssl_issue.py",
        "fixed_direct_fix.py",
        "one_step_ats_fix.py",
        "manual_fix_instructions.py",
        
        # Redundant test files
        "direct_ats_test.py",
        "simple_test_summary.py",
        "test_summary_simple.py",
        "test_tailored_summary.py",
        
        # Log files
        "ats_test.log"
    ]
    
    # Move files to backup directory
    moved_count = 0
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            # Create directory structure in backup if needed
            if "/" in file_path:
                dir_path = os.path.join(backup_dir, os.path.dirname(file_path))
                os.makedirs(dir_path, exist_ok=True)
            
            # Move file to backup
            backup_path = os.path.join(backup_dir, file_path)
            shutil.move(file_path, backup_path)
            print(f"✅ Moved to backup: {file_path}")
            moved_count += 1
        else:
            print(f"⚠️ File not found: {file_path}")
    
    # Clean up old output files (keep the most recent 5)
    output_dirs = ["output", "app/output", "app/static/output", "ats_test_output"]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            print(f"\n📂 Cleaning {output_dir} directory...")
            
            # Group files by type
            pdf_files = []
            txt_files = []
            json_files = []
            html_files = []
            other_files = []
            
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                if os.path.isfile(filepath):
                    if filename.endswith(".pdf"):
                        pdf_files.append(filepath)
                    elif filename.endswith(".txt"):
                        txt_files.append(filepath)
                    elif filename.endswith(".json"):
                        json_files.append(filepath)
                    elif filename.endswith(".html"):
                        html_files.append(filepath)
                    else:
                        other_files.append(filepath)
            
            # Keep only the 5 most recent files of each type
            for file_list in [pdf_files, txt_files, json_files, html_files, other_files]:
                if len(file_list) > 5:
                    # Sort by modification time (newest first)
                    file_list.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                    
                    # Move older files to backup
                    for old_file in file_list[5:]:
                        backup_path = os.path.join(backup_dir, old_file)
                        
                        # Create directory structure in backup
                        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                        
                        shutil.move(old_file, backup_path)
                        print(f"✅ Moved old file to backup: {old_file}")
                        moved_count += 1
    
    # Create a README in the backup directory
    readme_content = f"""# Backup Directory

This directory contains backup files created during project cleanup on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.

These files were moved here instead of being deleted to prevent accidental data loss.
You can safely delete this directory if you no longer need these files.
"""
    
    with open(os.path.join(backup_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    print(f"\n✅ Cleanup complete! Moved {moved_count} files to {backup_dir}")
    print(f"📝 You can safely delete {backup_dir} if you don't need the backed up files")

if __name__ == "__main__":
    cleanup_project()
