#!/usr/bin/env python3
"""
Simple Render deployment script
Handles directory and import issues
"""

import os
import sys
import subprocess

def main():
    """Simple deployment for Render"""
    
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Get the backend directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Current directory: {current_dir}")
    
    # Change to backend directory
    os.chdir(current_dir)
    print(f"📁 Changed to: {os.getcwd()}")
    
    # Add to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # List files to debug
    print("📋 Files in directory:")
    for file in os.listdir('.'):
        print(f"   - {file}")
    
    # Check for required files
    if not os.path.exists('app.py'):
        print("❌ app.py not found")
        sys.exit(1)
    
    if not os.path.exists('config.py'):
        print("❌ config.py not found")
        sys.exit(1)
    
    print("✅ Required files found")
    
    # Test import
    try:
        from app import app
        print("✅ App imported successfully")
    except Exception as e:
        print(f"❌ Failed to import app: {e}")
        sys.exit(1)
    
    print("🚀 Starting server...")
    
    # Use gunicorn with simple settings
    subprocess.run([
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:10000',
        '--workers', '1',
        '--timeout', '30',
        'app:app'
    ], cwd=current_dir)

if __name__ == "__main__":
    main() 