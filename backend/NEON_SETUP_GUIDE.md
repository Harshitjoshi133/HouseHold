# Neon Database Setup Guide

This guide will help you set up your PostgreSQL database on Neon using the generated SQL scripts.

## Step 1: Create Neon Database

1. **Go to https://neon.tech** and sign up/login
2. **Create a new project**:
   - Click "Create New Project"
   - Name: `household-services`
   - Region: Choose closest to your users
   - Click "Create Project"

3. **Get your connection string**:
   - Copy the connection string from your project dashboard
   - It looks like: `postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/database_name`

## Step 2: Configure Environment

1. **Update your `.env` file**:
   ```bash
   # Comment out SQLite
   # DATABASE_URL=sqlite:///instance/household_services.db
   
   # Add Neon connection string
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/database_name?sslmode=require
   ```

## Step 3: Create Database Structure

### Option A: Using Neon Console (Recommended)

1. **Open Neon Console**:
   - Go to your project dashboard
   - Click on "SQL Editor"

2. **Run the database creation script**:
   - Copy the contents of `create_postgresql_database.sql`
   - Paste it into the SQL Editor
   - Click "Run" to execute

### Option B: Using psql Command Line

1. **Install psql** (if not already installed):
   - Download from: https://www.postgresql.org/download/windows/
   - Add to PATH: `C:\Program Files\PostgreSQL\15\bin`

2. **Connect to Neon**:
   ```cmd
   psql "postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/database_name?sslmode=require"
   ```

3. **Run the SQL script**:
   ```cmd
   \i create_postgresql_database.sql
   ```

### Option C: Using Python Script

1. **Run the setup script**:
   ```cmd
   python setup_postgres.py
   ```

## Step 4: Verify Database Creation

1. **Check tables created**:
   ```sql
   \dt
   ```

2. **Check sample data**:
   ```sql
   SELECT * FROM services;
   ```

3. **Check admin user**:
   ```sql
   SELECT username, email, role FROM users WHERE role = 'admin';
   ```

## Step 5: Migrate Existing Data (Optional)

If you have data in your SQLite database:

1. **Export SQLite data**:
   ```cmd
   sqlite3 instance/household_services.db ".dump" > sqlite_export.sql
   ```

2. **Convert the export** to PostgreSQL format:
   - Replace `INTEGER` with `SERIAL` for primary keys
   - Replace `DATETIME` with `TIMESTAMP`
   - Remove SQLite-specific syntax

3. **Import to Neon**:
   - Use the SQL Editor in Neon Console
   - Or use the migration script: `migrate_data_to_postgres.sql`

## Step 6: Test Your Application

1. **Start your Flask app**:
   ```cmd
   python app.py
   ```

2. **Test API endpoints**:
   - Open browser to `http://localhost:5000/api/services`
   - Should return JSON data from PostgreSQL

## Step 7: Monitor Your Database

### Neon Dashboard Features:
- **Queries**: See real-time query performance
- **Usage**: Monitor connection and storage usage
- **Logs**: View database logs
- **Branches**: Create development branches

### Useful Neon Commands:
```sql
-- Check connection info
SELECT version();

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public';

-- Check active connections
SELECT * FROM pg_stat_activity;

-- Check table row counts
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables;
```

## Troubleshooting

### Common Issues:

1. **SSL Connection Error**:
   - Ensure `?sslmode=require` is in your connection string
   - Try `?sslmode=prefer` as alternative

2. **Connection Timeout**:
   - Check your internet connection
   - Verify the connection string
   - Try connecting from different network

3. **Permission Denied**:
   - Check if your user has proper permissions
   - Contact Neon support if needed

4. **Table Already Exists**:
   - Drop existing tables: `DROP TABLE IF EXISTS table_name CASCADE;`
   - Or use `CREATE TABLE IF NOT EXISTS`

### Performance Tips:

1. **Use Connection Pooling**:
   - Neon provides built-in connection pooling
   - Use the pooling endpoint in your connection string

2. **Optimize Queries**:
   - Use indexes for frequently queried columns
   - Monitor slow queries in Neon dashboard

3. **Monitor Usage**:
   - Keep track of your free tier limits
   - Upgrade if needed

## Security Best Practices

1. **Environment Variables**:
   - Never commit `.env` files to version control
   - Use different connection strings for dev/prod

2. **Database Security**:
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **Application Security**:
   - Validate all inputs
   - Use parameterized queries
   - Implement proper authentication

## Next Steps

After successful setup:

1. **Set up automated backups** (Neon handles this automatically)
2. **Configure monitoring** alerts
3. **Set up development branches** for testing
4. **Implement connection pooling** for better performance
5. **Set up CI/CD** for database migrations

## Support Resources

- **Neon Documentation**: https://neon.tech/docs/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Neon Community**: https://community.neon.tech/
- **Neon Status**: https://status.neon.tech/ 