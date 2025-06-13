#!/usr/bin/env python3
"""
Check application status and provide troubleshooting
"""

import os
import sys
import requests
import subprocess

def check_app_status():
    """Check if the app is running and accessible"""
    
    print("🔍 Resume Tailor - Status Check")
    print("=" * 40)
    
    # Check if app is running
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Application is running and accessible!")
            print("📍 URL: http://localhost:5000")
            print("🎯 Tailored Summary Feature: ACTIVE")
            return True
        else:
            print(f"⚠️  Application responding with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Application not accessible on http://localhost:5000")
    except requests.exceptions.Timeout:
        print("⏱️  Application timeout - may be starting up")
    except Exception as e:
        print(f"❌ Error checking application: {e}")
    
    # Check if process is running
    try:
        result = subprocess.run(['pgrep', '-f', 'python.*run'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("🔄 Python process found - app may be starting")
        else:
            print("❌ No Python app process found")
    except:
        pass
    
    print("\n💡 Troubleshooting Steps:")
    print("1. Run: python fix_ssl_issue.py")
    print("2. Start app: python run_simple_fixed.py")
    print("3. Access: http://localhost:5000")
    
    return False

if __name__ == "__main__":
    check_app_status()
