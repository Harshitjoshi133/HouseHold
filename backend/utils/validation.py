import re
from typing import Tuple, Dict, Any

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    return True, ""

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format"""
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""

def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """Validate phone number format"""
    if not phone:
        return False, "Phone number is required"
    
    # Remove spaces, dashes, and parentheses for validation
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    if len(cleaned_phone) < 10:
        return False, "Phone number must be at least 10 digits"
    
    if len(cleaned_phone) > 15:
        return False, "Phone number must be less than 15 digits"
    
    if not re.match(r'^[0-9+\-\s()]+$', phone):
        return False, "Phone number contains invalid characters"
    
    return True, ""

def validate_full_name(full_name: str) -> Tuple[bool, str]:
    """Validate full name"""
    if not full_name:
        return False, "Full name is required"
    
    if len(full_name) < 2:
        return False, "Full name must be at least 2 characters long"
    
    if len(full_name) > 100:
        return False, "Full name must be less than 100 characters"
    
    if not re.match(r'^[a-zA-Z\s]+$', full_name):
        return False, "Full name can only contain letters and spaces"
    
    return True, ""

def validate_address(address: str) -> Tuple[bool, str]:
    """Validate address"""
    if not address:
        return False, "Address is required"
    
    if len(address) < 5:
        return False, "Address must be at least 5 characters long"
    
    if len(address) > 200:
        return False, "Address must be less than 200 characters"
    
    return True, ""

def validate_pin_code(pin_code: str) -> Tuple[bool, str]:
    """Validate PIN code"""
    if not pin_code:
        return False, "PIN code is required"
    
    if len(pin_code) < 6:
        return False, "PIN code must be at least 6 characters"
    
    if len(pin_code) > 10:
        return False, "PIN code must be less than 10 characters"
    
    if not re.match(r'^[0-9]+$', pin_code):
        return False, "PIN code can only contain numbers"
    
    return True, ""

def validate_role(role: str) -> Tuple[bool, str]:
    """Validate user role"""
    valid_roles = ['customer', 'professional', 'admin']
    
    if not role:
        return False, "Role is required"
    
    if role not in valid_roles:
        return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
    
    return True, ""

def validate_service(service: str) -> Tuple[bool, str]:
    """Validate service name"""
    if not service:
        return False, "Service is required"
    
    if len(service) < 2:
        return False, "Service name must be at least 2 characters long"
    
    if len(service) > 100:
        return False, "Service name must be less than 100 characters"
    
    return True, ""

def validate_experience(experience: int) -> Tuple[bool, str]:
    """Validate experience years"""
    if experience is None:
        return False, "Experience is required"
    
    if experience < 0:
        return False, "Experience must be a positive number"
    
    if experience > 50:
        return False, "Experience cannot exceed 50 years"
    
    return True, ""

def validate_description(description: str) -> Tuple[bool, str]:
    """Validate description"""
    if not description:
        return False, "Description is required"
    
    if len(description) < 10:
        return False, "Description must be at least 10 characters long"
    
    if len(description) > 1000:
        return False, "Description must be less than 1000 characters"
    
    return True, ""

def validate_registration_data(data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    """Validate all registration fields"""
    errors = {}
    
    # Required fields validation
    required_fields = {
        'username': validate_username,
        'email': validate_email,
        'password': validate_password,
        'role': validate_role,
        'full_name': validate_full_name,
        'phone_number': validate_phone_number,
        'address': validate_address,
        'pin_code': validate_pin_code
    }
    
    for field, validator in required_fields.items():
        is_valid, error_msg = validator(data.get(field))
        if not is_valid:
            errors[field] = error_msg
    
    # Professional-specific validation
    if data.get('role') == 'professional':
        service_valid, service_error = validate_service(data.get('service', ''))
        if not service_valid:
            errors['service'] = service_error
        
        experience_valid, experience_error = validate_experience(data.get('experience', 0))
        if not experience_valid:
            errors['experience'] = experience_error
        
        description_valid, description_error = validate_description(data.get('description', ''))
        if not description_valid:
            errors['description'] = description_error
    
    return len(errors) == 0, errors

def validate_login_data(data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    """Validate login fields"""
    errors = {}
    
    email_valid, email_error = validate_email(data.get('email', ''))
    if not email_valid:
        errors['email'] = email_error
    
    password_valid, password_error = validate_password(data.get('password', ''))
    if not password_valid:
        errors['password'] = password_error
    
    return len(errors) == 0, errors 