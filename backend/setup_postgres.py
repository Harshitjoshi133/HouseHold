#!/usr/bin/env python3
"""
Setup script for PostgreSQL database
Usage: python setup_postgres.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_postgres():
    """Setup PostgreSQL database and run migrations"""
    
    postgres_url = os.environ.get('DATABASE_URL')
    
    if not postgres_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("Please set DATABASE_URL to your PostgreSQL connection string")
        print("Example: DATABASE_URL=postgresql://username:password@localhost:5432/household_services")
        return False
    
    # Fix postgres:// to postgresql:// if needed
    if postgres_url.startswith('postgres://'):
        postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("📊 Connecting to PostgreSQL database...")
        engine = create_engine(postgres_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ PostgreSQL connection successful")
        
        print("🔄 Running database migrations...")
        
        # Import Flask app and run migrations
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from flask_migrate import upgrade
            upgrade()
            print("✅ Database migrations completed")
        
        print("🎉 PostgreSQL setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL database...")
    success = setup_postgres()
    if success:
        print("✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("❌ Setup failed!")
        sys.exit(1) 