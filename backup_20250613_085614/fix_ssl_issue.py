#!/usr/bin/env python3
"""
Fix SSL/HTTPS issues for local development
"""

import os
import subprocess
import sys

def fix_ssl_issue():
    """Fix common SSL issues for local Flask development"""
    
    print("🔧 Fixing SSL/HTTPS Issues...")
    print("=" * 50)
    
    # Option 1: Run without SSL (simplest for development)
    print("\n1️⃣ RECOMMENDED: Run without SSL for development")
    print("   python run_simple.py")
    print("   Access at: http://localhost:5000")
    
    # Option 2: Generate self-signed certificates
    print("\n2️⃣ Generate self-signed SSL certificates:")
    print("   This will create cert.pem and key.pem files")
    
    try:
        # Check if OpenSSL is available
        result = subprocess.run(['openssl', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ OpenSSL available: {result.stdout.strip()}")
            
            # Generate self-signed certificate
            print("\n   Generating self-signed certificate...")
            cert_cmd = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
                '-keyout', 'key.pem', '-out', 'cert.pem',
                '-days', '365', '-nodes',
                '-subj', '/C=US/ST=State/L=City/O=Organization/CN=localhost'
            ]
            
            result = subprocess.run(cert_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ SSL certificates generated successfully!")
                print("   Files created: cert.pem, key.pem")
                print("   You can now run: python run_app.py")
                print("   Access at: https://localhost:5000")
                print("   (You'll need to accept the security warning)")
            else:
                print(f"   ❌ Error generating certificates: {result.stderr}")
        else:
            print("   ❌ OpenSSL not available")
            
    except FileNotFoundError:
        print("   ❌ OpenSSL not found on system")
    
    # Option 3: Use Flask development server without SSL
    print("\n3️⃣ Alternative: Modify Flask app to run on HTTP only")
    
    # Check current setup
    print("\n🔍 Current Setup Analysis:")
    if os.path.exists('run_simple.py'):
        print("   ✅ run_simple.py exists (HTTP only)")
    if os.path.exists('run_app.py'):
        print("   ✅ run_app.py exists (HTTPS)")
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print("   ✅ SSL certificates exist")
    else:
        print("   ❌ SSL certificates missing")
    
    print("\n💡 RECOMMENDATION:")
    print("   For development, use: python run_simple.py")
    print("   This runs on HTTP (no SSL) and should work without issues")
    
    return True

if __name__ == "__main__":
    fix_ssl_issue()
