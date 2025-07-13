#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to PostgreSQL
Usage: python migrate_to_postgres.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Get database URLs
    sqlite_url = 'sqlite:///instance/household_services.db'
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
        # Connect to SQLite database
        print("📊 Connecting to SQLite database...")
        sqlite_engine = create_engine(sqlite_url)
        sqlite_session = sessionmaker(bind=sqlite_engine)()
        
        # Connect to PostgreSQL database
        print("📊 Connecting to PostgreSQL database...")
        postgres_engine = create_engine(postgres_url)
        postgres_session = sessionmaker(bind=postgres_engine)()
        
        # Test PostgreSQL connection
        postgres_session.execute(text("SELECT 1"))
        print("✅ PostgreSQL connection successful")
        
        # Get all tables from SQLite
        result = sqlite_session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
        
        print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
        
        # Migrate each table
        for table in tables:
            print(f"🔄 Migrating table: {table}")
            
            # Get data from SQLite
            result = sqlite_session.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            
            if rows:
                # Get column names
                columns = result.keys()
                column_names = list(columns)
                
                # Insert data into PostgreSQL
                for row in rows:
                    data = dict(zip(column_names, row))
                    
                    # Build INSERT statement
                    placeholders = ', '.join([f':{col}' for col in column_names])
                    columns_str = ', '.join(column_names)
                    insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                    
                    try:
                        postgres_session.execute(text(insert_sql), data)
                    except Exception as e:
                        print(f"⚠️  Warning: Could not insert row in {table}: {e}")
                        continue
                
                postgres_session.commit()
                print(f"✅ Migrated {len(rows)} rows from {table}")
            else:
                print(f"ℹ️  Table {table} is empty")
        
        print("🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    finally:
        if 'sqlite_session' in locals():
            sqlite_session.close()
        if 'postgres_session' in locals():
            postgres_session.close()

if __name__ == "__main__":
    print("🚀 Starting SQLite to PostgreSQL migration...")
    success = migrate_data()
    if success:
        print("✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("❌ Migration failed!")
        sys.exit(1) 