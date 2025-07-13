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
    
    print("🚀 Starting Household Services (minimal deployment)...")
    print("📊 Avoiding problematic dependencies")
    
    # Use the most basic gunicorn setup
    subprocess.run([
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:10000',
        '--workers', '1',
        '--timeout', '30',
        '--preload',
        'app:app'
    ])

if __name__ == "__main__":
    main() 