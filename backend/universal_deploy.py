#!/usr/bin/env python3
"""
Universal deployment script that works on Windows and Linux
Automatically detects platform and uses appropriate server
"""

import os
import sys
import platform
import subprocess

def main():
    """Universal deployment for all platforms"""
    
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('FLASK_DEBUG', '0')
    
    # Get current directory and ensure we're in the backend directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"📁 Working directory: {current_dir}")
    
    # Check if required files exist
    required_files = ['app.py', 'config.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: {file} not found in {current_dir}")
            sys.exit(1)
    
    print("✅ All required files found")
    
    # Detect platform
    is_windows = platform.system() == 'Windows'
    is_linux = platform.system() == 'Linux'
    
    print(f"🖥️  Platform detected: {platform.system()}")
    
    if is_windows:
        print("🚀 Starting Household Services on Windows...")
        print("📊 Using Flask's built-in server")
        print("⚠️  Note: For production deployment, use Linux with Gunicorn")
        
        # Import and run with Flask's built-in server
        try:
            from app import app
            print("✅ App imported successfully")
            
            app.run(
                host='0.0.0.0',
                port=int(os.environ.get('PORT', 5000)),
                debug=False,
                threaded=True
            )
        except ImportError as e:
            print(f"❌ Failed to import app: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            sys.exit(1)
    
    elif is_linux:
        print("🚀 Starting Household Services on Linux...")
        print("📊 Using Gunicorn WSGI server")
        
        # Try to use gunicorn on Linux
        try:
            subprocess.run([
                sys.executable, '-m', 'gunicorn',
                '--bind', '0.0.0.0:10000',
                '--workers', '2',
                '--timeout', '30',
                'app:app'
            ], cwd=current_dir)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Gunicorn failed: {e}")
            print("🔄 Falling back to Flask's built-in server...")
            
            # Fallback to Flask's built-in server
            try:
                from app import app
                app.run(
                    host='0.0.0.0',
                    port=int(os.environ.get('PORT', 5000)),
                    debug=False,
                    threaded=True
                )
            except Exception as e2:
                print(f"❌ Flask server also failed: {e2}")
                sys.exit(1)
    
    else:
        print(f"❌ Unsupported platform: {platform.system()}")
        print("Please use Windows or Linux")
        sys.exit(1)

if __name__ == "__main__":
    main() 