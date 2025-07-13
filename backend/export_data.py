#!/usr/bin/env python3
"""
Database Export Script for Household Services
Usage: python export_data.py [format] [table_name]
"""

import os
import sys
import csv
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
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

def get_tables(engine):
    """Get list of tables in the database"""
    try:
        database_url = get_database_url()
        
        if 'sqlite' in database_url:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        else:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            tables = [row[0] for row in result.fetchall()]
            return tables
    except Exception as e:
        print(f"❌ Error getting tables: {e}")
        return []

def export_to_csv(engine, table_name, filename=None):
    """Export table data to CSV"""
    if not filename:
        filename = f"export_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        query = f"SELECT * FROM {table_name}"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(rows)
        
        print(f"✅ Exported {len(rows)} rows to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return None

def export_to_json(engine, table_name, filename=None):
    """Export table data to JSON"""
    if not filename:
        filename = f"export_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        query = f"SELECT * FROM {table_name}"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
        
        # Convert rows to list of dictionaries
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Handle datetime objects
                if isinstance(value, datetime):
                    value = value.isoformat()
                row_dict[str(col)] = value
            data.append(row_dict)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(data)} rows to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return None

def export_to_sql(engine, table_name, filename=None):
    """Export table data to SQL INSERT statements"""
    if not filename:
        filename = f"export_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    try:
        query = f"SELECT * FROM {table_name}"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
        
        with open(filename, 'w', encoding='utf-8') as sqlfile:
            sqlfile.write(f"-- Export of table {table_name}\n")
            sqlfile.write(f"-- Generated on {datetime.now().isoformat()}\n\n")
            
            for row in rows:
                values = []
                for value in row:
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, str):
                        values.append(f"'{value.replace(chr(39), chr(39)+chr(39))}'")
                    elif isinstance(value, datetime):
                        values.append(f"'{value.isoformat()}'")
                    else:
                        values.append(str(value))
                
                columns_str = ', '.join(str(col) for col in columns)
                values_str = ', '.join(values)
                sqlfile.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
        
        print(f"✅ Exported {len(rows)} rows to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error exporting to SQL: {e}")
        return None

def export_all_tables(engine, format_type):
    """Export all tables in the specified format"""
    tables = get_tables(engine)
    
    if not tables:
        print("❌ No tables found in database")
        return
    
    print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
    
    for table in tables:
        print(f"\n🔄 Exporting table: {table}")
        
        if format_type == 'csv':
            export_to_csv(engine, table)
        elif format_type == 'json':
            export_to_json(engine, table)
        elif format_type == 'sql':
            export_to_sql(engine, table)

def main():
    """Main function"""
    print("📤 Database Export Tool for Household Services")
    print("=" * 50)
    
    # Get database connection
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    # Test connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\n📋 Usage:")
        print("  python export_data.py csv [table_name]")
        print("  python export_data.py json [table_name]")
        print("  python export_data.py sql [table_name]")
        print("  python export_data.py all [format]")
        print("\n💡 Examples:")
        print("  python export_data.py csv users")
        print("  python export_data.py json services")
        print("  python export_data.py all csv")
        return
    
    format_type = sys.argv[1].lower()
    
    if format_type not in ['csv', 'json', 'sql']:
        print("❌ Invalid format. Use: csv, json, or sql")
        return
    
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'all':
            # Export all tables
            export_all_tables(engine, format_type)
        else:
            # Export specific table
            table_name = sys.argv[2]
            print(f"🔄 Exporting table '{table_name}' to {format_type.upper()}")
            
            if format_type == 'csv':
                export_to_csv(engine, table_name)
            elif format_type == 'json':
                export_to_json(engine, table_name)
            elif format_type == 'sql':
                export_to_sql(engine, table_name)
    else:
        # Show available tables and let user choose
        tables = get_tables(engine)
        if not tables:
            print("❌ No tables found in database")
            return
        
        print(f"\n📋 Available tables: {', '.join(tables)}")
        print(f"💡 To export all tables: python export_data.py {format_type} all")
        print(f"💡 To export specific table: python export_data.py {format_type} table_name")

if __name__ == "__main__":
    main() 