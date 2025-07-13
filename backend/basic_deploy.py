#!/usr/bin/env python3
"""
Basic deployment script - runs Flask app directly
"""

import os
import sys

def main():
    """Basic deployment"""
    
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Get the backend directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Add to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"📁 Working directory: {current_dir}")
    
    # Import and run the app
    try:
        from app import app
        print("✅ App imported successfully")
        
        # Run the app
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 10000)),
            debug=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 