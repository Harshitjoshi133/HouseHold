# Error Handling and Logging Guide

This guide covers the comprehensive error handling and logging system implemented in the Household Services application.

## 📋 **Overview**

The application now includes:
- **Centralized logging** with multiple log levels
- **File rotation** to manage log file sizes
- **Error tracking** with context information
- **Security event logging** for audit trails
- **Performance monitoring** with metrics
- **Graceful error handling** with proper HTTP responses

## 🗂️ **Log Files Structure**

```
backend/
├── logs/
│   ├── app.log          # All application logs (DEBUG and above)
│   ├── errors.log       # Error logs only (ERROR and above)
│   └── database.log     # Database operation logs
```

## 📊 **Log Levels**

### **DEBUG** - Detailed debugging information
- Function entry/exit
- Database query details
- Request/response data

### **INFO** - General application information
- Application startup/shutdown
- User actions (login, registration)
- API requests and responses
- Task completion

### **WARNING** - Potential issues
- Failed login attempts
- Missing required fields
- Deprecated feature usage

### **ERROR** - Error conditions
- Database connection failures
- API errors
- Task failures
- Security violations

### **CRITICAL** - Application-breaking errors
- Startup failures
- Critical system errors

## 🔧 **Logging Functions**

### **Basic Logging**
```python
from logger import setup_logger

logger = setup_logger('my_module')

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### **Error Logging with Context**
```python
from logger import log_error_with_context

try:
    # Your code here
    pass
except Exception as e:
    log_error_with_context(e, {
        "user_id": user.id,
        "action": "profile_update",
        "data": request_data
    })
```

### **Security Event Logging**
```python
from logger import log_security_event

# Log security events
log_security_event("failed_login", "Invalid password for user@example.com", "WARNING")
log_security_event("successful_login", "User logged in: john_doe", "INFO")
log_security_event("unauthorized_access", "Attempted access to admin panel", "ERROR")
```

### **Performance Metrics**
```python
from logger import log_performance_metric

# Log performance metrics
log_performance_metric("api_response_time", 150, "ms")
log_performance_metric("database_query_time", 25, "ms")
```

## 🎯 **Decorators for Automatic Logging**

### **API Request Logging**
```python
from logger import log_api_request

@app.route('/api/users', methods=['GET'])
@log_api_request
def get_users():
    # Your code here
    pass
```

### **Function Call Logging**
```python
from logger import log_function_call

@log_function_call
def process_user_data(user_id, data):
    # Your code here
    pass
```

### **Database Operation Logging**
```python
from logger import log_database_operation

@log_database_operation("SELECT")
def get_user_by_id(user_id):
    # Your code here
    pass
```

## 🚨 **Error Handling Patterns**

### **1. API Route Error Handling**
```python
@app.route('/api/users', methods=['POST'])
@log_api_request
def create_user():
    try:
        data = request.json
        
        # Validate input
        if not data.get('email'):
            logger.warning("User creation failed - missing email")
            return jsonify({'error': 'Email is required'}), 400
        
        # Process request
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"User created successfully: {user.email}")
        return jsonify({'message': 'User created'}), 201
        
    except Exception as e:
        logger.error(f"User creation failed: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/users",
            "method": "POST",
            "data": data if 'data' in locals() else None
        })
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500
```

### **2. Database Error Handling**
```python
def get_user_profile(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            return None
        
        return user
        
    except Exception as e:
        logger.error(f"Database query failed for user {user_id}: {e}")
        log_error_with_context(e, {
            "function": "get_user_profile",
            "user_id": user_id
        })
        raise
```

### **3. Task Error Handling**
```python
@shared_task(bind=True)
def process_background_task(self):
    try:
        # Task logic here
        result = perform_task()
        
        logger.info("Background task completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Background task failed: {e}")
        log_error_with_context(e, {"task": "process_background_task"})
        
        # Retry with exponential backoff
        raise self.retry(countdown=60, max_retries=3, exc=e)
```

## 🔍 **Monitoring and Debugging**

### **Health Check Endpoint**
```bash
# Check application health
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "database": "healthy",
  "redis": "healthy",
  "version": "1.0.0"
}
```

### **Log Analysis Commands**
```bash
# View recent errors
tail -f logs/errors.log

# Search for specific errors
grep "ERROR" logs/app.log

# Monitor API requests
grep "API Request" logs/app.log

# Check database operations
tail -f logs/database.log
```

## 🛡️ **Security Logging**

### **Authentication Events**
- Successful logins
- Failed login attempts
- Password changes
- Account lockouts

### **Authorization Events**
- Unauthorized access attempts
- Permission denied events
- Admin actions

### **Data Access Events**
- Sensitive data access
- Bulk data operations
- Data export/import

## 📈 **Performance Monitoring**

### **Response Time Tracking**
```python
import time

def track_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = (time.time() - start_time) * 1000
        
        log_performance_metric(f"{func.__name__}_execution_time", execution_time, "ms")
        return result
    return wrapper
```

### **Database Query Monitoring**
```python
@log_database_operation("SELECT")
def get_user_data(user_id):
    # Database query here
    pass
```

## 🔧 **Configuration**

### **Log Level Configuration**
```python
# In your .env file
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### **Log File Rotation**
- **app.log**: 10MB max, 5 backup files
- **errors.log**: 5MB max, 3 backup files
- **database.log**: 5MB max, 3 backup files

## 🚀 **Best Practices**

### **1. Always Log Errors with Context**
```python
try:
    # Your code
    pass
except Exception as e:
    log_error_with_context(e, {
        "user_id": user.id,
        "action": "data_processing",
        "input_data": data
    })
```

### **2. Use Appropriate Log Levels**
```python
logger.debug("Detailed debugging info")
logger.info("General information")
logger.warning("Potential issues")
logger.error("Error conditions")
logger.critical("Application-breaking errors")
```

### **3. Include Relevant Context**
```python
logger.info(f"User {user.username} performed action {action}")
logger.warning(f"Rate limit exceeded for IP {request.remote_addr}")
```

### **4. Handle Database Transactions Properly**
```python
try:
    # Database operations
    db.session.commit()
except Exception as e:
    db.session.rollback()
    logger.error(f"Database transaction failed: {e}")
    raise
```

### **5. Monitor Application Health**
```bash
# Regular health checks
curl http://localhost:5000/health

# Log file monitoring
tail -f logs/app.log | grep ERROR
```

## 📊 **Log Analysis Tools**

### **Simple Log Analysis**
```bash
# Count errors by type
grep "ERROR" logs/app.log | cut -d'|' -f4 | sort | uniq -c

# Find slow API calls
grep "API Response" logs/app.log | grep -E "[0-9]+\.[0-9]+s"

# Monitor user activity
grep "User logged in" logs/app.log
```

### **Advanced Log Analysis**
```python
import re
from datetime import datetime

def analyze_logs(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    errors = []
    for line in lines:
        if 'ERROR' in line:
            # Parse error information
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*ERROR.*: (.*)', line)
            if match:
                errors.append({
                    'timestamp': match.group(1),
                    'message': match.group(2)
                })
    
    return errors
```

## 🔄 **Maintenance**

### **Log Rotation**
Logs are automatically rotated when they reach the configured size limits. Old log files are kept for the specified number of backups.

### **Log Cleanup**
```python
# Clean up old logs (older than 30 days)
import os
from datetime import datetime, timedelta

def cleanup_old_logs():
    cutoff_date = datetime.now() - timedelta(days=30)
    log_dir = 'logs'
    
    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)
        if os.path.getmtime(filepath) < cutoff_date.timestamp():
            os.remove(filepath)
            logger.info(f"Removed old log file: {filename}")
```

This comprehensive error handling and logging system ensures that your application is robust, debuggable, and maintainable in production environments. 