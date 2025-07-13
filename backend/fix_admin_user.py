#!/usr/bin/env python3
"""
Script to fix admin user and ensure proper authentication
Usage: python fix_admin_user.py
"""

import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User
from logger import setup_logger

logger = setup_logger('fix_admin')

def fix_admin_user():
    """Fix admin user password and ensure proper setup"""
    try:
        with app.app_context():
            # Check if admin user exists
            admin = User.query.filter_by(role='admin').first()
            
            if admin:
                logger.info(f"Admin user found: {admin.username}")
                
                # Set a proper password
                admin.set_password('admin123')
                admin.is_active = True
                admin.email = 'admin@example.com'
                
                db.session.commit()
                logger.info("Admin password updated successfully")
                
                # Test the password
                if admin.check_password('admin123'):
                    logger.info("✅ Admin password verification successful")
                else:
                    logger.error("❌ Admin password verification failed")
                    
            else:
                logger.info("Creating new admin user...")
                
                # Create new admin user
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin',
                    full_name='Administrator',
                    is_active=True
                )
                admin.set_password('admin123')
                
                db.session.add(admin)
                db.session.commit()
                
                logger.info("✅ New admin user created successfully")
            
            # Display admin credentials
            print("\n" + "="*50)
            print("🔐 ADMIN CREDENTIALS")
            print("="*50)
            print(f"Username: admin")
            print(f"Email: admin@example.com")
            print(f"Password: admin123")
            print("="*50)
            print("💡 Use these credentials to login to the admin panel")
            print("="*50 + "\n")
            
            return True
            
    except Exception as e:
        logger.error(f"Failed to fix admin user: {e}")
        return False

def test_admin_login():
    """Test admin login functionality"""
    try:
        with app.app_context():
            admin = User.query.filter_by(role='admin').first()
            
            if not admin:
                logger.error("No admin user found")
                return False
            
            # Test password check
            if admin.check_password('admin123'):
                logger.info("✅ Admin login test successful")
                return True
            else:
                logger.error("❌ Admin login test failed")
                return False
                
    except Exception as e:
        logger.error(f"Admin login test failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Admin User...")
    
    # Fix admin user
    if fix_admin_user():
        print("✅ Admin user fixed successfully")
        
        # Test login
        if test_admin_login():
            print("✅ Admin login test passed")
        else:
            print("❌ Admin login test failed")
    else:
        print("❌ Failed to fix admin user")
        sys.exit(1)

if __name__ == "__main__":
    main() 