#!/usr/bin/env python3
"""
WSGI entry point for production deployment
Usage with Gunicorn: gunicorn wsgi:app
Usage with uWSGI: uwsgi --ini uwsgi.ini
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app import app

# Configure for production
if __name__ == "__main__":
    # Only for local testing - use proper WSGI server in production
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 