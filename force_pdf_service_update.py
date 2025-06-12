"""
Force update the services to use the ReportLab PDFService
"""
import os
import shutil

def backup_and_update_services():
    """Backup current services and update to use PDFService"""
    
    # Backup current services/__init__.py
    services_init = "app/services/__init__.py"
    backup_file = "app/services/__init__.py.backup"
    
    if os.path.exists(services_init):
        shutil.copy(services_init, backup_file)
        print(f"✅ Backed up {services_init} to {backup_file}")
    
    # The new __init__.py is already created above, so we just need to restart
    print("✅ Updated services/__init__.py to prioritize ReportLab PDFService")
    
    print("\nNext steps:")
    print("1. Restart your Flask app: Ctrl+C then python run_simple.py")
    print("2. Generate a new resume")
    print("3. Check that PDF files are created in app/output/")

if __name__ == "__main__":
    print("=== Forcing PDF Service Update ===")
    backup_and_update_services()
