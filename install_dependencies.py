#!/usr/bin/env python3
"""
Install required dependencies for the ATS optimization test
"""

import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    
    # List of required packages
    packages = [
        "colorama",
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("\n✅ All dependencies installed successfully!")
    print("You can now run the test_ats_optimization.py script")
    
    return True

if __name__ == "__main__":
    install_dependencies()
