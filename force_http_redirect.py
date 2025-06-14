#!/usr/bin/env python3
"""
Force HTTP redirect for development
"""

import webbrowser
import time
import subprocess
import sys

def open_http_browser():
    """Open browser with HTTP URL"""
    
    print("🌐 Opening browser with HTTP URL...")
    
    # URLs to try
    urls = [
        "http://localhost:5000",
        "http://127.0.0.1:5000", 
        "http://localhost:5000/profile"
    ]
    
    for url in urls:
        print(f"📍 Trying: {url}")
        try:
            webbrowser.open(url)
            print(f"✅ Opened: {url}")
            break
        except Exception as e:
            print(f"❌ Failed to open {url}: {e}")
    
    print("\n💡 If you still see security warnings:")
    print("   1. Look for 'Advanced' button and click it")
    print("   2. Click 'Continue to localhost (unsafe)'")
    print("   3. Or manually type: http://localhost:5000/profile")

if __name__ == "__main__":
    open_http_browser()
