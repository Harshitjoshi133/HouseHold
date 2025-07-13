# API Validation Guide

This guide provides the correct request/response formats for all API endpoints with proper validation.

## 🔐 **Authentication Endpoints**

### **1. User Registration**
**Endpoint**: `POST /api/auth/register`

**Required Fields**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "customer",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "address": "123 Main St",
  "pin_code": "12345"
}
```

**Optional Fields**:
- `phone_number`
- `address`
- `pin_code`

**For Professional Registration**:
```json
{
  "username": "plumber_joe",
  "email": "joe@plumbing.com",
  "password": "securepassword123",
  "role": "professional",
  "full_name": "Joe Plumber",
  "service": "Plumbing",
  "experience": 5,
  "description": "Experienced plumber with 5 years of experience"
}
```

**Response (Success - 201)**:
```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "customer",
    "full_name": "John Doe",
    "is_active": true
  }
}
```

**Response (Error - 400)**:
```json
{
  "error": "Missing required fields: username, email"
}
```

### **2. User Login**
**Endpoint**: `POST /api/auth/login`

**Request**:
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response (Success - 200)**:
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "full_name": "Administrator"
  }
}
```

**Response (Error - 401)**:
```json
{
  "error": "Invalid email or password"
}
```

### **3. Get User Profile**
**Endpoint**: `GET /api/auth/profile`
**Headers**: `Authorization: Bearer <token>`

**Response (Success - 200)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "customer",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "address": "123 Main St",
  "pin_code": "12345",
  "is_active": true
}
```

### **4. Update User Profile**
**Endpoint**: `PUT /api/auth/profile`
**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "full_name": "John Updated",
  "phone_number": "+1234567890",
  "address": "456 New St",
  "pin_code": "54321"
}
```

## 📋 **Service Endpoints**

### **1. Get All Services**
**Endpoint**: `GET /api/services`

**Response (Success - 200)**:
```json
[
  {
    "id": 1,
    "name": "Plumbing",
    "price": 50,
    "description": "Fixing pipes and leaks"
  },
  {
    "id": 2,
    "name": "Electrician",
    "price": 40,
    "description": "Wiring and electrical fixes"
  }
]
```

## 🏥 **Health Check**

### **1. Application Health**
**Endpoint**: `GET /health`

**Response (Healthy - 200)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "database": "healthy",
  "redis": "healthy",
  "version": "1.0.0"
}
```

**Response (Degraded - 503)**:
```json
{
  "status": "degraded",
  "timestamp": "2024-01-15T10:30:00",
  "database": "healthy",
  "redis": "unhealthy: Connection failed",
  "version": "1.0.0"
}
```

## 🔧 **Testing with curl**

### **1. Test Admin Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### **2. Test User Registration**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "customer",
    "full_name": "Test User"
  }'
```

### **3. Test Health Check**
```bash
curl http://localhost:5000/health
```

### **4. Test Services API**
```bash
curl http://localhost:5000/api/services
```

## 🚨 **Common Error Responses**

### **400 Bad Request**
```json
{
  "error": "Bad Request",
  "message": "The request could not be processed",
  "timestamp": "2024-01-15T10:30:00"
}
```

### **401 Unauthorized**
```json
{
  "error": "Unauthorized",
  "message": "Authentication required",
  "timestamp": "2024-01-15T10:30:00"
}
```

### **404 Not Found**
```json
{
  "error": "Not Found",
  "message": "The requested resource was not found",
  "timestamp": "2024-01-15T10:30:00"
}
```

### **500 Internal Server Error**
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 📝 **Validation Rules**

### **Username**
- Required
- Must be unique
- 3-64 characters
- Alphanumeric and underscores only

### **Email**
- Required
- Must be unique
- Valid email format
- Maximum 120 characters

### **Password**
- Required
- Minimum 6 characters
- Should contain letters and numbers

### **Role**
- Required
- Must be one of: `customer`, `professional`, `admin`

### **Full Name**
- Required
- 2-100 characters
- Letters, spaces, and hyphens only

### **Phone Number**
- Optional
- International format recommended
- Maximum 20 characters

### **Address**
- Optional
- Maximum 200 characters

### **Pin Code**
- Optional
- Maximum 10 characters

## 🔍 **Debugging Tips**

### **1. Check Request Headers**
```bash
curl -v -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

### **2. Monitor Logs**
```bash
# View real-time logs
tail -f logs/app.log

# Check for specific errors
grep "ERROR" logs/errors.log

# Monitor API requests
grep "API Request" logs/app.log
```

### **3. Test with Postman/Insomnia**
- Use the exact JSON format shown above
- Include proper Content-Type headers
- Check response status codes and messages

## 🎯 **Quick Fix Commands**

### **Fix Admin User**
```bash
python fix_admin_user.py
```

### **Test API Endpoints**
```bash
# Test health
curl http://localhost:5000/health

# Test services
curl http://localhost:5000/api/services

# Test admin login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

This guide ensures that all API requests are properly formatted and validated. 