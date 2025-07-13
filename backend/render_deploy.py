#!/usr/bin/env python3
"""
Render deployment script for Household Services
This script is specifically designed for Render deployment
"""

import os
import sys
import subprocess

def main():
    """Deploy the application on Render"""
    
    # Set production environment variables
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Get the current directory (should be the backend directory)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Working directory: {current_dir}")
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Check if required files exist
    required_files = ['app.py', 'config.py', 'wsgi.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: {file} not found in {current_dir}")
            sys.exit(1)
    
    print("✅ All required files found")
    
    # Try to import the app to test
    try:
        from app import app
        print("✅ App imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        print(f"Python path: {sys.path}")
        sys.exit(1)
    
    # Start the application
    print("🚀 Starting Household Services on Render...")
    print("📊 Server will be available at the Render URL")
    print("🔧 Using Gunicorn WSGI server")
    
    try:
        # Use gunicorn with simplified configuration for Render
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '--bind', '0.0.0.0:10000',  # Render uses port 10000
            '--workers', '4',
            '--timeout', '30',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'wsgi:app'
        ], cwd=current_dir)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 