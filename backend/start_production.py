#!/usr/bin/env python3
"""
Production startup script for Household Services
Usage: python start_production.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the application in production mode"""
    
    # Set production environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ Error: app.py not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Check if gunicorn is available
    try:
        import gunicorn
        print("✅ Gunicorn is available")
    except ImportError:
        print("❌ Gunicorn not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn==21.2.0'])
    
    print("🚀 Starting Household Services in production mode...")
    print("📊 Server will be available at: http://0.0.0.0:5000")
    print("🔧 Using Gunicorn WSGI server")
    print("📋 API endpoints available at /api/*")
    print("\nPress Ctrl+C to stop the server")
    
    # Start Gunicorn
    try:
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '-c', 'gunicorn.conf.py',
            'wsgi:app'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 