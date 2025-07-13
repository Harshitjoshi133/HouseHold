# PostgreSQL Migration Guide (Windows + Cloud)

This guide will help you migrate your household services application from SQLite to PostgreSQL, optimized for Windows and cloud hosting.

## Prerequisites

1. **Windows System Requirements**:
   - Windows 10/11
   - Python 3.8+ installed
   - Git Bash or PowerShell

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Option 1: Cloud PostgreSQL (Recommended)

### Neon Database (Recommended)

Neon is a serverless PostgreSQL with a generous free tier and excellent performance.

1. **Create Neon Account**:
   - Go to https://neon.tech
   - Sign up with GitHub, Google, or email
   - Verify your email

2. **Create New Project**:
   - Click "Create New Project"
   - Choose a project name (e.g., `household-services`)
   - Select your region (choose closest to your users)
   - Click "Create Project"

3. **Get Connection Details**:
   - After project creation, you'll see your connection string
   - It looks like: `postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/database_name`
   - Copy the connection string for your `.env` file

4. **Neon-Specific Features**:
   - **Branching**: Create database branches for development/testing
   - **Auto-scaling**: Automatically scales based on usage
   - **Point-in-time restore**: Restore to any point in time
   - **Connection pooling**: Built-in connection pooling

### AWS RDS PostgreSQL

1. **Create RDS Instance**:
   - Go to AWS Console → RDS → Create database
   - Choose PostgreSQL
   - Select Free tier (if available) or appropriate tier
   - Configure security group to allow your IP

2. **Get Connection Details**:
   ```bash
   # Your connection string will look like:
   DATABASE_URL=postgresql://username:password@your-instance.region.rds.amazonaws.com:5432/database_name
   ```

### Azure Database for PostgreSQL

1. **Create Azure Database**:
   - Go to Azure Portal → Create resource → Azure Database for PostgreSQL
   - Choose Basic tier for cost efficiency
   - Configure firewall rules

2. **Connection String**:
   ```bash
   DATABASE_URL=postgresql://username@server-name.postgres.database.azure.com:5432/database_name
   ```

### Heroku Postgres

1. **Create Heroku App** (if you don't have one):
   ```bash
   heroku create your-app-name
   ```

2. **Add PostgreSQL Add-on**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Get Database URL**:
   ```bash
   heroku config:get DATABASE_URL
   ```

### Railway PostgreSQL

1. **Create Railway Account** at railway.app
2. **Create New Project** → Add PostgreSQL
3. **Get Connection String** from the PostgreSQL service

### Supabase (Free Tier Available)

1. **Create Supabase Project** at supabase.com
2. **Get Connection String** from Settings → Database

## Option 2: Local PostgreSQL (Windows)

### Install PostgreSQL on Windows

1. **Download PostgreSQL**:
   - Go to https://www.postgresql.org/download/windows/
   - Download the installer for Windows x86-64

2. **Install PostgreSQL**:
   - Run the installer as Administrator
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\15`)
   - Set password for `postgres` user (remember this!)
   - Keep default port 5432
   - Complete installation

3. **Verify Installation**:
   - Open Command Prompt
   - Navigate to PostgreSQL bin directory:
   ```cmd
   cd "C:\Program Files\PostgreSQL\15\bin"
   ```
   - Test connection:
   ```cmd
   psql -U postgres -h localhost
   ```

### Create Local Database

1. **Open pgAdmin** (installed with PostgreSQL):
   - Start → PostgreSQL 15 → pgAdmin 4

2. **Create Database**:
   - Right-click on "Databases" → Create → Database
   - Name: `household_services`
   - Click Save

3. **Create User** (optional):
   - Right-click on "Login/Group Roles" → Create → Login/Group Role
   - Name: `household_user`
   - Password: `your_password`
   - Privileges tab: Can login = Yes

## Step 3: Configure Environment

1. **Copy the environment template**:
   ```cmd
   copy .env-template .env
   ```

2. **Edit `.env` file** with your database URL:

   **For Neon Database**:
   ```bash
   # Comment out SQLite
   # DATABASE_URL=sqlite:///instance/household_services.db
   
   # Neon Database (replace with your actual connection string)
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/database_name?sslmode=require
   ```

   **For Other Cloud PostgreSQL**:
   ```bash
   # Cloud PostgreSQL (replace with your actual connection string)
   DATABASE_URL=postgresql://username:password@host:5432/database_name
   ```

   **For Local PostgreSQL**:
   ```bash
   # Local PostgreSQL
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/household_services
   ```

## Step 4: Initialize Database

### For Neon Database

1. **Run the setup script**:
   ```cmd
   python setup_postgres.py
   ```

2. **Neon-specific SSL configuration**:
   - Neon requires SSL connections
   - The connection string should include `?sslmode=require`
   - If you get SSL errors, ensure your connection string has the SSL parameter

3. **Verify connection in Neon Console**:
   - Go to your Neon project dashboard
   - Check the "Queries" tab to see your application's queries
   - Monitor connection usage in the "Usage" tab

### For Other Cloud PostgreSQL

1. **Run the setup script**:
   ```cmd
   python setup_postgres.py
   ```

2. **If you get SSL errors**, add `?sslmode=require` to your connection string:
   ```bash
   DATABASE_URL=postgresql://username:password@host:5432/database_name?sslmode=require
   ```

### For Local PostgreSQL

1. **Ensure PostgreSQL service is running**:
   - Open Services (services.msc)
   - Find "postgresql-x64-15" service
   - Ensure it's running

2. **Run setup script**:
   ```cmd
   python setup_postgres.py
   ```

## Step 5: Migrate Data (Optional)

If you have existing SQLite data:

1. **Run migration script**:
   ```cmd
   python migrate_to_postgres.py
   ```

2. **Verify migration** by checking your data

## Step 6: Test Application

1. **Start Flask application**:
   ```cmd
   python app.py
   ```

2. **Test API endpoints**:
   - Open browser to `http://localhost:5000/api/services`
   - Should return JSON data

## Windows-Specific Troubleshooting

### Common Windows Issues

1. **"psql is not recognized"**:
   - Add PostgreSQL to PATH:
   ```cmd
   setx PATH "%PATH%;C:\Program Files\PostgreSQL\15\bin"
   ```
   - Restart Command Prompt

2. **"Connection refused"**:
   - Check if PostgreSQL service is running:
   ```cmd
   services.msc
   ```
   - Find "postgresql-x64-15" and ensure it's running

3. **"Authentication failed"**:
   - Double-check password in connection string
   - Try connecting with pgAdmin first

4. **SSL Connection Issues** (Cloud):
   - Add SSL parameters to connection string:
   ```bash
   DATABASE_URL=postgresql://username:password@host:5432/database_name?sslmode=require&sslcert=&sslkey=&sslrootcert=
   ```

### Neon-Specific Issues

1. **"Connection timeout"**:
   - Check your internet connection
   - Verify the connection string from Neon dashboard
   - Ensure you're using the correct region

2. **"SSL certificate verification failed"**:
   - Neon requires SSL, ensure `?sslmode=require` is in your connection string
   - Try using `?sslmode=prefer` as an alternative

3. **"Too many connections"**:
   - Neon has connection limits on free tier
   - Implement connection pooling in your application
   - Monitor connections in Neon dashboard

### Useful Windows Commands

**Check PostgreSQL status**:
```cmd
sc query postgresql-x64-15
```

**Start PostgreSQL service**:
```cmd
net start postgresql-x64-15
```

**Stop PostgreSQL service**:
```cmd
net stop postgresql-x64-15
```

**Connect to PostgreSQL**:
```cmd
psql -U postgres -d household_services -h localhost
```

## Cloud-Specific Tips

### Neon Database
- **Free tier**: 3 projects, 0.5GB storage, 10GB transfer/month
- **Branching**: Create separate branches for dev/staging/prod
- **Connection pooling**: Use Neon's built-in pooling
- **Auto-scaling**: Automatically scales based on usage
- **Point-in-time restore**: Restore to any moment in time

### AWS RDS
- Use security groups to control access
- Enable encryption at rest
- Set up automated backups

### Azure Database
- Use Azure Key Vault for secrets
- Enable geo-replication if needed
- Monitor with Azure Monitor

### Heroku
- Use connection pooling for better performance
- Set up automated backups
- Monitor with Heroku add-ons

### Railway/Supabase
- Use connection pooling
- Set up monitoring
- Configure backups

## Performance Optimization

1. **Connection Pooling** (for production):
   ```python
   # Add to requirements.txt
   psycopg2-binary==2.9.9
   ```

2. **Environment Variables** for cloud:
   ```bash
   # Add to .env
   DATABASE_POOL_SIZE=20
   DATABASE_MAX_OVERFLOW=30
   ```

3. **Neon-specific optimization**:
   - Use Neon's connection pooling endpoint
   - Monitor query performance in Neon dashboard
   - Use appropriate indexes for your queries

## Rollback to SQLite

If you need to switch back:

1. **Update `.env` file**:
   ```bash
   DATABASE_URL=sqlite:///instance/household_services.db
   ```

2. **Restart application**

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong passwords** for database users
3. **Enable SSL** for cloud connections
4. **Regular backups** of your database
5. **Monitor connection logs** for suspicious activity
6. **Neon-specific**: Use connection pooling to reduce connection overhead

## Next Steps

After successful migration:

1. **Set up automated backups**
2. **Configure monitoring** (CPU, memory, connections)
3. **Set up alerts** for database issues
4. **Consider read replicas** for high-traffic applications
5. **Implement connection pooling** for better performance
6. **Neon-specific**: Set up database branching for development workflows

## Support Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Neon Documentation**: https://neon.tech/docs/
- **AWS RDS Documentation**: https://docs.aws.amazon.com/rds/
- **Azure Database Documentation**: https://docs.microsoft.com/en-us/azure/postgresql/
- **Heroku Postgres**: https://devcenter.heroku.com/categories/heroku-postgres 