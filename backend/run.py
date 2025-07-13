#!/usr/bin/env python3
"""
Simple run script for the Flask application with comprehensive error handling
Usage: python run.py
"""

import os
import sys
import signal
import atexit
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import logger first
from logger import setup_logger, log_error_with_context

# Initialize logger
logger = setup_logger('run_script')

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def cleanup():
    """Cleanup function called on exit"""
    logger.info("Application shutdown complete")

def main():
    """Main application entry point"""
    try:
        logger.info("🚀 Starting Household Services Application...")
        logger.info("📊 Server will be available at: http://localhost:5000")
        logger.info("📋 API endpoints:")
        logger.info("   - GET  /api/services")
        logger.info("   - POST /api/auth/login")
        logger.info("   - POST /api/auth/register")
        logger.info("   - GET  /api/admin/dashboard")
        logger.info("   - GET  /api/customer/dashboard")
        logger.info("   - GET  /api/professional/dashboard")
        logger.info("   - GET  /health")
        logger.info("\nPress Ctrl+C to stop the server")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Register cleanup function
        atexit.register(cleanup)
        
        # Import and run the app
        from app import app
        
        # Start the Flask application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        logger.critical(f"Failed to import application modules: {e}")
        log_error_with_context(e, {"stage": "module_import"})
        print("❌ Failed to import application modules. Please check your dependencies.")
        sys.exit(1)
        
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        log_error_with_context(e, {"stage": "application_startup"})
        print("❌ Failed to start application. Check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 