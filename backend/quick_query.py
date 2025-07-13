#!/usr/bin/env python3
"""
Quick Database Query Script
Usage: python quick_query.py "SELECT * FROM users"
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment or use SQLite default"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        print(f"Database URL: {database_url}")
        # Fix postgres:// to postgresql:// if needed
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    else:
        # Default to SQLite
        return 'sqlite:///instance/household_services.db'

def execute_query(query):
    """Execute a SQL query and return results"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
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

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🔍 Quick Database Query Tool")
        print("Usage: python quick_query.py \"SELECT * FROM users\"")
        print("\n📋 Sample queries:")
        print("  python quick_query.py \"SELECT * FROM users\"")
        print("  python quick_query.py \"SELECT * FROM services\"")
        print("  python quick_query.py \"SELECT COUNT(*) FROM users\"")
        print("  python quick_query.py \"SELECT * FROM customers c JOIN users u ON c.user_id = u.id\"")
        return
    
    query = sys.argv[1]
    print(f"🔍 Executing query: {query}")
    
    columns, rows = execute_query(query)
    if columns:
        print(f"\n📊 Results ({len(rows)} rows):")
        print(format_results(columns, rows))
    else:
        print("❌ Query failed or returned no results.")

if __name__ == "__main__":
    main() 