from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import csv
import io
import datetime

from models import db, User, Service, Professional, Customer, ServiceRequest
from tasks import  send_monthly_report

admin_bp = Blueprint('admin', __name__)
import redis
import hashlib
import json

redis_client=redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
def cache_key(route, params):
    return f"{route}:{hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()}"
def cache_response(key, data, ttl=300):
    redis_client.setex(key, ttl, json.dumps(data))
    print(f"Cached response for:{key}")
def get_cached_response(key):
    cached_data=redis_client.get(key)
    if cached_data:
        print(f"Cache HIT:{key}")
        return json.loads(cached_data)
    print(f"Cache MISS:{key}")
    return None

# Middleware to check if user is admin


def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
            
        return fn(*args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper

# Service management
@admin_bp.route('/services', methods=['POST'])
def create_service():
    data = request.json
    
    service = Service(
        name=data.get('name'),
        price=data.get('price'),
        time_required=data.get('time_required'),
        description=data.get('description')
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'message': 'Service created successfully',
        'service': service.to_dict()
    }), 201

@admin_bp.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404
        
    data = request.json
    
    # Update service fields
    for field in ['name', 'price', 'time_required', 'description']:
        if field in data:
            setattr(service, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service updated successfully',
        'service': service.to_dict()
    }), 200

@admin_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    db.session.delete(service)
    db.session.commit()
    
    return jsonify({'message': 'Service deleted successfully'}), 200

@admin_bp.route('/services', methods=['GET'])
def get_services():
    key = cache_key('/services', request.args)
    cached_data = get_cached_response(key)
    if cached_data:
        return jsonify(cached_data), 200

    services = Service.query.all()
    response = [service.to_dict() for service in services]

    cache_response(key, response)
    return jsonify(response), 200

# Professional management
@admin_bp.route('/professionals', methods=['GET'])
def get_professionals():
    professionals = Professional.query.all()
    response = [prof.to_dict() for prof in professionals]
    return jsonify(response), 200


@admin_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    response = [cust.to_dict() for cust in customers]
    return jsonify(response), 200


@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response = {'users': [user.to_dict() for user in users]}
    return jsonify(response), 200

@admin_bp.route('/requests', methods=['GET'])
def get_requests():
    key = cache_key('/requests', request.args)
    cached_data = get_cached_response(key)
    if cached_data:
        return jsonify(cached_data), 200

    servicerequests = ServiceRequest.query.all()
    response = [servicerequest.to_dict() for servicerequest in servicerequests]

    cache_response(key, response)
    return jsonify(response), 200


@admin_bp.route('/professionals/<int:professional_id>/verify', methods=['PUT'])
def verify_professional(professional_id):
    professional = Professional.query.filter_by(id=professional_id).first()
    print(professional)
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404  
    print(professional.is_verified)
    if(professional.is_verified==True):
        professional.is_verified = False
    else:
        professional.is_verified = True
    db.session.commit()
    print(professional.is_verified)
    return jsonify({
        'message': 'Professional verified successfully',
        'professional': professional.to_dict()
    }), 200
@admin_bp.route('/users/<int:user_id>/block', methods=['PUT'])
def block_user(user_id):
    
    customer=Customer.query.filter_by(id=user_id).first()
    user = User.query.filter_by(id=customer.user_id).first()
    if not user:
        print(user)
        return jsonify({'error': 'User not found'}), 404
    
    if user.role == 'admin':
        return jsonify({'error': 'Cannot block admin user'}), 403
    if not customer:
        print(customer)
        return jsonify({'dikkat':'customer not found'}),400
    customer.is_blocked = True
    db.session.commit()
    
    print(customer.to_dict())
    
    return jsonify({
        'message': 'User blocked successfully',
        'user': user.to_dict(),
        'customer':customer.to_dict()
    }), 200


@admin_bp.route('/users/<int:user_id>/unblock', methods=['PUT'])
def unblock_user(user_id):
    customer=Customer.query.filter_by(id=user_id).first()
    user = User.query.filter_by(id=customer.user_id).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    customer.is_blocked = False
    db.session.commit()
    print(user.to_dict())

    return jsonify({
        'message': 'User unblocked successfully',
        'user': user.to_dict()
    }), 200

# Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_data():
    total_customers = Customer.query.count()
    total_professionals = Professional.query.count()
    total_services = Service.query.count()
    total_service_requests = ServiceRequest.query.count()
    
    pending_verifications = Professional.query.filter_by(is_verified=False).count()
    
    recent_requests = ServiceRequest.query.order_by(ServiceRequest.date_of_request.desc()).limit(5).all()
    
    return jsonify({
        'total_customers': total_customers,
        'total_professionals': total_professionals,
        'total_services': total_services,
        'total_service_requests': total_service_requests,
        'pending_verifications': pending_verifications,
        'recent_requests': [req.to_dict() for req in recent_requests]
    }), 200


# Trigger monthly report
@admin_bp.route('/trigger-monthly-report', methods=['POST']) 
@admin_required
def trigger_monthly_report():
    # Get all customers
    customers = Customer.query.all()
    customer_ids = [c.id for c in customers]
    
    task = send_monthly_report.delay(customer_ids)
    
    return jsonify({
        'message': 'Monthly report generation started',
        'task_id': task.id
    }), 202



@admin_bp.route('/completed-service-requests/', methods=['GET'])
def get_completed_service_requests():
    completed_requests = ServiceRequest.query.all()
    
    return jsonify([request.to_dict() for request in completed_requests]), 200