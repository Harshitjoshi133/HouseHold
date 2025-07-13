from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Customer, Professional,Service
from logger import log_api_request, log_error_with_context, log_security_event, setup_logger
from utils.validation import validate_registration_data, validate_login_data

auth_bp = Blueprint('auth', __name__)
logger = setup_logger('auth')

@auth_bp.route('/register', methods=['POST'])
@log_api_request
def register():
    """Register a new user"""
    try:
        data = request.json
        logger.info(f"Registration attempt for email: {data.get('email', 'unknown')}")
        
        # Validate all registration data
        is_valid, validation_errors = validate_registration_data(data)
        if not is_valid:
            logger.warning(f"Registration failed - validation errors: {validation_errors}")
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=data.get('username')).first()
        if existing_username:
            logger.warning(f"Registration failed - username already exists: {data.get('username')}")
            log_security_event("duplicate_username", f"Attempt to register existing username: {data.get('username')}", "WARNING")
            return jsonify({'error': f'Username {data.get("username")} already exists'}), 400
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=data.get('email')).first()
        if existing_email:
            logger.warning(f"Registration failed - email already exists: {data.get('email')}")
            log_security_event("duplicate_email", f"Attempt to register existing email: {data.get('email')}", "WARNING")
            return jsonify({'error': f'Email {data.get("email")} already exists'}), 400
        
        # Hash password
        hashed_password = generate_password_hash(data.get('password'))
        
        # Create new user
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            pin_code=data.get('pin_code'),
            role=data.get('role'),
            password_hash=hashed_password
        )
        
        db.session.add(user)
        db.session.flush()  # Flush to get user.id
        
        # Create profile based on role
        if user.role == 'customer':
            customer = Customer(user_id=user.id)
            db.session.add(customer)
            logger.info(f"Customer profile created for user: {user.id}")
        elif user.role == 'professional':
            service_name = data.get('service')
            
            # Check if service exists
            service_query = Service.query.filter_by(name=service_name).first()
            if not service_query:
                logger.error(f"Registration failed - service not found: {service_name}")
                db.session.rollback()
                return jsonify({'error': f'Service {service_name} not found'}), 400
            
            # Check if the user is already in professionals
            existing_professional = Professional.query.filter_by(user_id=user.id).first()
            if existing_professional:
                logger.warning(f"Registration failed - user already professional: {user.id}")
                db.session.rollback()
                return jsonify({'error': 'User is already registered as a professional'}), 400
            
            professional = Professional(
                user_id=user.id,
                service_id=service_query.id,
                experience=data.get('experience', 0),
                description=data.get('description', ''),
                is_verified=False
            )
            db.session.add(professional)
            logger.info(f"Professional profile created for user: {user.id}")
        
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        logger.info(f"User registered successfully: {user.username} ({user.role})")
        log_security_event("user_registration", f"New user registered: {user.username} ({user.role})", "INFO")
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/auth/register",
            "method": "POST",
            "data": data if 'data' in locals() else None
        })
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@auth_bp.route('/login', methods=['POST'])
@log_api_request
def login():
    """User login"""
    try:
        data = request.json
        logger.info(f"Login attempt for email: {data.get('email', 'unknown')}")
        
        # Validate login data
        is_valid, validation_errors = validate_login_data(data)
        if not is_valid:
            logger.warning(f"Login failed - validation errors: {validation_errors}")
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            logger.warning(f"Login failed - user not found: {email}")
            log_security_event("failed_login", f"Login attempt with non-existent email: {email}", "WARNING")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.check_password(password):
            logger.warning(f"Login failed - invalid password for user: {email}")
            log_security_event("failed_login", f"Login attempt with wrong password for: {email}", "WARNING")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            logger.warning(f"Login failed - inactive user: {email}")
            log_security_event("inactive_user_login", f"Login attempt for inactive user: {email}", "WARNING")
            return jsonify({'error': 'Account is deactivated'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        logger.info(f"User logged in successfully: {user.username}")
        log_security_event("successful_login", f"User logged in: {user.username}", "INFO")
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/auth/login",
            "method": "POST",
            "email": data.get('email') if 'data' in locals() else None
        })
        return jsonify({'error': 'Login failed. Please try again.'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@log_api_request
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            logger.warning(f"Profile request failed - user not found: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        logger.info(f"Profile retrieved for user: {user.username}")
        profile_data = user.to_dict()
        return jsonify(profile_data), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/auth/profile",
            "method": "GET",
            "user_id": get_jwt_identity() if 'get_jwt_identity' in locals() else None
        })
        return jsonify({'error': 'Failed to retrieve profile'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@log_api_request
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            logger.warning(f"Profile update failed - user not found: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        data = request.json
        logger.info(f"Profile update request for user: {user.username}")
        
        # Update basic user fields
        for field in ['full_name', 'phone_number', 'address', 'pin_code']:
            if field in data:
                setattr(user, field, data[field])
        
        # Update role-specific fields
        if user.role == 'customer' and user.customer_profile:
            if 'preferences' in data:
                user.customer_profile.preferences = data['preferences']
        elif user.role == 'professional' and user.professional_profile:
            if 'experience' in data:
                user.professional_profile.experience = data['experience']
            if 'description' in data:
                user.professional_profile.description = data['description']
        
        db.session.commit()
        
        logger.info(f"Profile updated successfully for user: {user.username}")
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/auth/profile",
            "method": "PUT",
            "user_id": get_jwt_identity() if 'get_jwt_identity' in locals() else None
        })
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@log_api_request
def logout():
    """User logout"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user:
            logger.info(f"User logged out: {user.username}")
            log_security_event("user_logout", f"User logged out: {user.username}", "INFO")
        else:
            logger.warning(f"Logout for non-existent user: {user_id}")
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        log_error_with_context(e, {
            "endpoint": "/api/auth/logout",
            "method": "POST"
        })
        return jsonify({'error': 'Logout failed'}), 500
