# Production Deployment Guide

## Overview
This guide explains how to deploy the Household Services application in production using proper WSGI servers and security configurations.

## Why not use `run.py` in production?

The `run.py` file is designed for **development only** because it:
- Uses Flask's built-in development server (not production-ready)
- Has debug mode enabled (security risk)
- Lacks proper process management
- Doesn't handle concurrent requests efficiently

## Production Setup

### 1. Install Production Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Set these environment variables for production:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-secure-secret-key
export DATABASE_URL=your-production-database-url
export REDIS_URL=your-production-redis-url
```

### 3. Production Startup Options

#### Option A: Using the Production Script
```bash
python start_production.py
```

#### Option B: Direct Gunicorn Command
```bash
gunicorn -c gunicorn.conf.py wsgi:app
```

#### Option C: Simple Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

### 4. Process Management (Recommended)

#### Using systemd (Linux)
Create `/etc/systemd/system/household-services.service`:
```ini
[Unit]
Description=Household Services API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/your/app/backend
Environment=FLASK_ENV=production
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable household-services
sudo systemctl start household-services
```

#### Using Supervisor
Create `/etc/supervisor/conf.d/household-services.conf`:
```ini
[program:household-services]
command=/path/to/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
directory=/path/to/your/app/backend
user=your-user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/household-services.log
```

### 5. Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/household-services`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/household-services /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Security Considerations

### 1. Environment Variables
- Never commit secrets to version control
- Use environment variables for all sensitive data
- Consider using a secrets management service

### 2. Database Security
- Use strong passwords
- Enable SSL connections
- Restrict database access to application servers only

### 3. CORS Configuration
The application is configured to allow specific origins:
- `https://house-hold-one.vercel.app` (your frontend)
- Local development URLs

### 4. Rate Limiting
Consider adding rate limiting middleware for API endpoints.

## Monitoring and Logging

### 1. Application Logs
- Logs are written to stdout/stderr
- Configure log rotation
- Monitor for errors and performance issues

### 2. Health Checks
Use the `/health` endpoint to monitor application status:
```bash
curl http://your-domain.com/health
```

### 3. Database Monitoring
Monitor database connections and query performance.

## Performance Optimization

### 1. Database
- Use connection pooling
- Optimize queries
- Consider read replicas for heavy read loads

### 2. Caching
- Redis is configured for session storage and caching
- Consider implementing API response caching

### 3. Static Files
- Serve static files through Nginx
- Enable compression
- Set proper cache headers

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Permission denied**
   ```bash
   sudo chown -R your-user:your-user /path/to/app
   ```

3. **Database connection issues**
   - Check DATABASE_URL environment variable
   - Verify database server is running
   - Check firewall settings

### Log Locations
- Application logs: Check your process manager logs
- Nginx logs: `/var/log/nginx/`
- System logs: `journalctl -u household-services`

## Backup Strategy

### 1. Database Backups
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Application Code
- Use version control (Git)
- Tag releases for easy rollback

### 3. Configuration
- Backup environment variables
- Document all configuration changes

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected (if applicable)
- [ ] SSL certificates installed
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Health checks passing
- [ ] CORS configured for frontend
- [ ] Rate limiting configured (optional)
- [ ] Log rotation configured
- [ ] Process manager configured
- [ ] Reverse proxy configured 