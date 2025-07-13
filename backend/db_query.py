#!/usr/bin/env python3
"""
Database Query Script for Household Services
Usage: python db_query.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment or use SQLite default"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Fix postgres:// to postgresql:// if needed
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    else:
        # Default to SQLite
        return 'sqlite:///instance/household_services.db'

def create_connection():
    """Create database connection"""
    try:
        database_url = get_database_url()
        print(f"🔗 Connecting to: {database_url.split('@')[0]}...")
        
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        return engine
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def execute_query(engine, query, params=None):
    """Execute a SQL query and return results"""
    try:
        with engine.connect() as conn:
            if params:
                result = conn.execute(text(query), params)
            else:
                result = conn.execute(text(query))
            
            # Get column names
            columns = result.keys()
            
            # Fetch all rows
            rows = result.fetchall()
            
            return columns, rows
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        return None, None

def format_results(columns, rows):
    """Format query results for display"""
    if not rows:
        return "No results found."
    
    # Create table header
    header = " | ".join(str(col) for col in columns)
    separator = "-" * len(header)
    
    # Create table rows
    table_rows = []
    for row in rows:
        formatted_row = " | ".join(str(cell) if cell is not None else "NULL" for cell in row)
        table_rows.append(formatted_row)
    
    return f"{header}\n{separator}\n" + "\n".join(table_rows)

def get_sample_queries():
    """Get sample queries for different tables"""
    return {
        "1": {
            "name": "List all users",
            "query": "SELECT id, username, email, role, full_name, created_at FROM users LIMIT 10"
        },
        "2": {
            "name": "List all services",
            "query": "SELECT id, name, price, description FROM services"
        },
        "3": {
            "name": "List all customers",
            "query": "SELECT c.id, u.username, u.email, u.full_name, c.is_blocked FROM customers c JOIN users u ON c.user_id = u.id"
        },
        "4": {
            "name": "List all professionals",
            "query": "SELECT p.id, u.username, u.full_name, s.name as service_name, p.is_verified, p.avg_rating FROM professionals p JOIN users u ON p.user_id = u.id JOIN services s ON p.service_id = s.id"
        },
        "5": {
            "name": "List all service requests",
            "query": "SELECT sr.id, s.name as service_name, sr.status, sr.date_of_request, sr.scheduled_date FROM service_requests sr JOIN services s ON sr.service_id = s.id ORDER BY sr.date_of_request DESC LIMIT 10"
        },
        "6": {
            "name": "List all reviews",
            "query": "SELECT r.id, r.rating, r.comment, r.created_at FROM reviews r ORDER BY r.created_at DESC LIMIT 10"
        },
        "7": {
            "name": "Count records by table",
            "query": "SELECT 'users' as table_name, COUNT(*) as count FROM users UNION ALL SELECT 'services', COUNT(*) FROM services UNION ALL SELECT 'customers', COUNT(*) FROM customers UNION ALL SELECT 'professionals', COUNT(*) FROM professionals UNION ALL SELECT 'service_requests', COUNT(*) FROM service_requests UNION ALL SELECT 'reviews', COUNT(*) FROM reviews"
        },
        "8": {
            "name": "Recent service requests with details",
            "query": """
            SELECT 
                sr.id,
                s.name as service_name,
                cu.username as customer_username,
                pu.username as professional_username,
                sr.status,
                sr.date_of_request
            FROM service_requests sr
            JOIN services s ON sr.service_id = s.id
            JOIN customers c ON sr.customer_id = c.id
            JOIN users cu ON c.user_id = cu.id
            LEFT JOIN professionals p ON sr.professional_id = p.id
            LEFT JOIN users pu ON p.user_id = pu.id
            ORDER BY sr.date_of_request DESC
            LIMIT 10
            """
        },
        "9": {
            "name": "Professional ratings",
            "query": """
            SELECT 
                u.full_name,
                s.name as service_name,
                p.avg_rating,
                COUNT(r.id) as review_count
            FROM professionals p
            JOIN users u ON p.user_id = u.id
            JOIN services s ON p.service_id = s.id
            LEFT JOIN service_requests sr ON p.id = sr.professional_id
            LEFT JOIN reviews r ON sr.id = r.service_request_id
            GROUP BY p.id, u.full_name, s.name, p.avg_rating
            ORDER BY p.avg_rating DESC
            """
        },
        "10": {
            "name": "Custom query",
            "query": "SELECT 'Enter your custom SQL query here' as message"
        }
    }

def main():
    """Main function"""
    print("🔍 Database Query Tool for Household Services")
    print("=" * 50)
    
    # Create database connection
    engine = create_connection()
    if not engine:
        return
    
    # Get sample queries
    sample_queries = get_sample_queries()
    
    while True:
        print("\n📋 Available queries:")
        for key, query_info in sample_queries.items():
            print(f"  {key}. {query_info['name']}")
        
        print("\n💡 Options:")
        print("  'q' - Quit")
        print("  'c' - Custom query")
        print("  't' - Show table structure")
        
        choice = input("\n🎯 Enter your choice (1-10, q, c, t): ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        
        elif choice == 'c':
            custom_query = input("🔍 Enter your SQL query: ").strip()
            if custom_query:
                columns, rows = execute_query(engine, custom_query)
                if columns:
                    print(f"\n📊 Results ({len(rows)} rows):")
                    print(format_results(columns, rows))
            continue
        
        elif choice == 't':
            show_table_structure(engine)
            continue
        
        elif choice in sample_queries:
            query_info = sample_queries[choice]
            print(f"\n🔍 Executing: {query_info['name']}")
            print(f"📝 Query: {query_info['query']}")
            
            columns, rows = execute_query(engine, query_info['query'])
            if columns:
                print(f"\n📊 Results ({len(rows)} rows):")
                print(format_results(columns, rows))
        
        else:
            print("❌ Invalid choice. Please try again.")

def show_table_structure(engine):
    """Show database table structure"""
    try:
        database_url = get_database_url()
        
        if 'sqlite' in database_url:
            # SQLite table structure
            query = """
            SELECT 
                name as table_name,
                sql as table_schema
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        else:
            # PostgreSQL table structure
            query = """
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            ORDER BY table_name, ordinal_position
            """
        
        columns, rows = execute_query(engine, query)
        if columns:
            print(f"\n📋 Database Structure ({len(rows)} tables/columns):")
            print(format_results(columns, rows))
    
    except Exception as e:
        print(f"❌ Error showing table structure: {e}")

if __name__ == "__main__":
    main() 