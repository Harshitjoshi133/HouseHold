#!/usr/bin/env python3
"""
Test script for validation functions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.validation import (
    validate_email, validate_password, validate_username, 
    validate_phone_number, validate_full_name, validate_address,
    validate_pin_code, validate_role, validate_service,
    validate_experience, validate_description,
    validate_registration_data, validate_login_data
)

def test_validation_functions():
    """Test all validation functions"""
    
    print("Testing validation functions...\n")
    
    # Test email validation
    print("=== Email Validation ===")
    test_emails = [
        ("test@example.com", True),
        ("invalid-email", False),
        ("test@", False),
        ("@example.com", False),
        ("", False)
    ]
    
    for email, expected in test_emails:
        is_valid, error = validate_email(email)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {email}: {is_valid} (expected: {expected})")
        if not is_valid:
            print(f"  Error: {error}")
    
    # Test password validation
    print("\n=== Password Validation ===")
    test_passwords = [
        ("password123", True),
        ("123", False),
        ("", False),
        ("a" * 129, False)  # Too long
    ]
    
    for password, expected in test_passwords:
        is_valid, error = validate_password(password)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {password}: {is_valid} (expected: {expected})")
        if not is_valid:
            print(f"  Error: {error}")
    
    # Test username validation
    print("\n=== Username Validation ===")
    test_usernames = [
        ("john_doe", True),
        ("john", True),
        ("jo", False),
        ("john@doe", False),
        ("", False)
    ]
    
    for username, expected in test_usernames:
        is_valid, error = validate_username(username)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {username}: {is_valid} (expected: {expected})")
        if not is_valid:
            print(f"  Error: {error}")
    
    # Test registration data validation
    print("\n=== Registration Data Validation ===")
    
    # Valid customer registration
    valid_customer_data = {
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'password123',
        'role': 'customer',
        'full_name': 'John Doe',
        'phone_number': '1234567890',
        'address': '123 Main St',
        'pin_code': '123456'
    }
    
    is_valid, errors = validate_registration_data(valid_customer_data)
    print(f"Valid customer registration: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Invalid customer registration
    invalid_customer_data = {
        'username': 'jo',  # Too short
        'email': 'invalid-email',
        'password': '123',  # Too short
        'role': 'invalid_role',
        'full_name': 'J',  # Too short
        'phone_number': '123',  # Too short
        'address': '123',  # Too short
        'pin_code': '123'  # Too short
    }
    
    is_valid, errors = validate_registration_data(invalid_customer_data)
    print(f"Invalid customer registration: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Valid professional registration
    valid_professional_data = {
        'username': 'jane_pro',
        'email': 'jane@example.com',
        'password': 'password123',
        'role': 'professional',
        'full_name': 'Jane Smith',
        'phone_number': '1234567890',
        'address': '456 Oak Ave',
        'pin_code': '654321',
        'service': 'Plumbing',
        'experience': 5,
        'description': 'Experienced plumber with 5 years of service'
    }
    
    is_valid, errors = validate_registration_data(valid_professional_data)
    print(f"Valid professional registration: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Test login data validation
    print("\n=== Login Data Validation ===")
    
    valid_login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    is_valid, errors = validate_login_data(valid_login_data)
    print(f"Valid login data: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    invalid_login_data = {
        'email': 'invalid-email',
        'password': '123'
    }
    
    is_valid, errors = validate_login_data(invalid_login_data)
    print(f"Invalid login data: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    print("\n=== Validation Test Complete ===")

if __name__ == "__main__":
    test_validation_functions() 