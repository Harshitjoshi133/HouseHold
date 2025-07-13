#!/usr/bin/env python3
"""
Simple deployment script for Render
Just runs gunicorn with basic settings
"""

import os
import sys
import subprocess

def main():
    """Simple deployment for Render"""
    
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Import compatibility module early
    try:
        import compat
        print("✅ Compatibility module loaded")
    except ImportError:
        print("⚠️  Compatibility module not found, continuing...")
    
    print("🚀 Starting Household Services...")
    print("📊 Using simple gunicorn deployment")
    
    # Simple gunicorn command for Render
    subprocess.run([
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:10000',
        '--workers', '2',
        '--timeout', '30',
        'app:app'
    ])

if __name__ == "__main__":
    main() 