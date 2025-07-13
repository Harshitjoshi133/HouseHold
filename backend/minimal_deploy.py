#!/usr/bin/env python3
"""
Minimal deployment script that avoids problematic dependencies
"""

import os
import sys
import subprocess

def main():
    """Minimal deployment avoiding fcntl issues"""
    
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Disable celery to avoid fcntl issues
    os.environ.setdefault('CELERY_DISABLE', '1')
    
    # Get current directory and ensure we're in the backend directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"📁 Working directory: {current_dir}")
    print("🚀 Starting Household Services (minimal deployment)...")
    print("📊 Avoiding problematic dependencies")
    
    # Check if required files exist
    required_files = ['app.py', 'config.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: {file} not found in {current_dir}")
            sys.exit(1)
    
    print("✅ All required files found")
    
    # Use the most basic gunicorn setup
    subprocess.run([
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:10000',
        '--workers', '1',
        '--timeout', '30',
        '--preload',
        'app:app'
    ], cwd=current_dir)

if __name__ == "__main__":
    main() 