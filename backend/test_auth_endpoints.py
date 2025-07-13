#!/usr/bin/env python3
"""
Test script for authentication endpoints with validation
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_registration_validation():
    """Test registration endpoint with various validation scenarios"""
    
    print("=== Testing Registration Validation ===\n")
    
    # Test 1: Valid customer registration
    print("Test 1: Valid Customer Registration")
    valid_customer_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "password123",
        "role": "customer",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "address": "123 Test Street",
        "pin_code": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=valid_customer_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 2: Invalid registration (missing fields)
    print("Test 2: Invalid Registration - Missing Fields")
    invalid_data = {
        "username": "test",
        "email": "invalid-email",
        "password": "123",
        "role": "invalid_role"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=invalid_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 3: Valid professional registration
    print("Test 3: Valid Professional Registration")
    valid_professional_data = {
        "username": "prouser123",
        "email": "pro@example.com",
        "password": "password123",
        "role": "professional",
        "full_name": "Professional User",
        "phone_number": "9876543210",
        "address": "456 Pro Street",
        "pin_code": "654321",
        "service": "Plumbing",
        "experience": 5,
        "description": "Experienced plumber with 5 years of service in residential and commercial plumbing."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=valid_professional_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_login_validation():
    """Test login endpoint with various validation scenarios"""
    
    print("=== Testing Login Validation ===\n")
    
    # Test 1: Valid login
    print("Test 1: Valid Login")
    valid_login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=valid_login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 2: Invalid login (wrong email format)
    print("Test 2: Invalid Login - Wrong Email Format")
    invalid_login_data = {
        "email": "invalid-email",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=invalid_login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 3: Invalid login (short password)
    print("Test 3: Invalid Login - Short Password")
    invalid_password_data = {
        "email": "test@example.com",
        "password": "123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=invalid_password_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_duplicate_registration():
    """Test duplicate registration scenarios"""
    
    print("=== Testing Duplicate Registration ===\n")
    
    # Test duplicate username
    print("Test 1: Duplicate Username")
    duplicate_username_data = {
        "username": "testuser123",  # Same as previous test
        "email": "different@example.com",
        "password": "password123",
        "role": "customer",
        "full_name": "Different User",
        "phone_number": "1111111111",
        "address": "Different Address",
        "pin_code": "111111"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=duplicate_username_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test duplicate email
    print("Test 2: Duplicate Email")
    duplicate_email_data = {
        "username": "differentuser",
        "email": "test@example.com",  # Same as previous test
        "password": "password123",
        "role": "customer",
        "full_name": "Different User",
        "phone_number": "2222222222",
        "address": "Different Address",
        "pin_code": "222222"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=duplicate_email_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def main():
    """Run all tests"""
    print("Authentication Endpoint Validation Tests")
    print("=" * 50)
    print()
    
    test_registration_validation()
    test_login_validation()
    test_duplicate_registration()
    
    print("=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main() 