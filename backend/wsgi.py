#!/usr/bin/env python3
"""
WSGI entry point for production deployment
Usage with Gunicorn: gunicorn wsgi:app
Usage with uWSGI: uwsgi --ini uwsgi.ini
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import compatibility module early to handle fcntl issues
try:
    import compat
    print("✅ Compatibility module loaded")
except ImportError:
    print("⚠️  Compatibility module not found, continuing...")

# Set environment variables for production
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', '0')

# Import the Flask app
try:
    from app import app
except ImportError as e:
    print(f"Error importing app: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    raise

# Configure for production
if __name__ == "__main__":
    # Only for local testing - use proper WSGI server in production
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 