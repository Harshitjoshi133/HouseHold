from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from models import db, User, Professional, ServiceRequest

professional_bp = Blueprint('professional', __name__)

# Middleware to check if user is a professional
def professional_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'professional':
            return jsonify({'error': 'Professional access required'}), 403
            
        return fn(user, *args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper

@professional_bp.route('/details/<int:user_id>',methods=['GET'])
def get_profile(user_id):
    user=User.query.filter_by(id=user_id).first()
    professional=Professional.query.filter_by(user_id=user_id).first()
    print(user)
    print(professional)
    return jsonify({
        "message":"Fetch Successfully",
        "user":user.to_dict(),
        "professional":professional.to_dict()
    }),200




# Upload verification document
@professional_bp.route('/upload-document', methods=['POST'])
def upload_document():
    user_id=request.form.get('user_id')

    professional = Professional.query.filter_by(user_id=user_id).first()
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    if 'document' not in request.files:
        return jsonify({'error': 'No document part'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(f"{user_id}_{file.filename}")
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        professional.document_path = filename
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document_path': filename
        }), 200

# Get pending service requests
@professional_bp.route('/service-requests/pending/<int:user_id>', methods=['GET'])
def get_pending_service_requests(user_id):
    professional = Professional.query.filter_by(user_id=user_id).first()
    print(professional)
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    # Only verified professionals can see service requests
    if not professional.is_verified:
        return jsonify({'error': 'Your profile is not verified yet'}), 403
    user=User.query.filter_by(id=user_id).first()
    print(user)
    # Get service requests that match the professional's service type and location
    service_requests = ServiceRequest.query.filter_by(
        service_id=professional.service_id,
        status='requested'
    ).all()
    print(service_requests)
    return jsonify([request.to_dict() for request in service_requests]), 200

# Get professional's assigned service requests
@professional_bp.route('/service-requests/<int:user_id>', methods=['GET'])
def get_assigned_service_requests(user_id):
    user=User.query.filter_by(id=user_id).first()
    professional = user.professional_profile
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    status_filter = request.args.get('status')
    
    query = ServiceRequest.query.filter_by(professional_id=professional.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    service_requests = query.order_by(ServiceRequest.scheduled_date.desc()).all()
    
    return jsonify({
        'service_requests': [request.to_dict() for request in service_requests]
    }), 200

# Accept service request
@professional_bp.route('/service-requests/<int:request_id>/accept/<int:user_id>', methods=['PUT'])
def accept_service_request(user_id, request_id):
    user=User.query.filter_by(id=user_id).first()
    professional = user.professional_profile
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    # Only verified professionals can accept requests
    if not professional.is_verified:
        return jsonify({'error': 'Your profile is not verified yet'}), 403
    
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    if service_request.status != 'requested':
        return jsonify({'error': 'Service request is not in requested status'}), 400
    
    if service_request.service_id != professional.service_id:
        return jsonify({'error': 'Service request does not match your service type'}), 400
    
    service_request.professional_id = professional.id
    service_request.status = 'accepted'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service request accepted successfully',
        'service_request': service_request.to_dict()
    }), 200

# Reject service request
@professional_bp.route('/service-requests/<int:request_id>/reject/<int:user_id>', methods=['PUT'])
def reject_service_request(request_id,user_id):
    user=User.query.filter_by(id=user_id).first()
    professional = user.professional_profile
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    print(professional.id)
    print(service_request.professional_id)
    service_request.professional_id = None
    service_request.status = 'requested'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service request rejected successfully',
        'service_request': service_request.to_dict()
    }), 200




@professional_bp.route('/service-requests/accepted/<int:user_id>', methods=['GET'])
def get_accepted_service_requests(user_id):
    professional = Professional.query.filter_by(user_id=user_id).first()
    
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    print(professional.id)
    accepted_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='accepted').all()
    print(accepted_requests)
    return jsonify([request.to_dict() for request in accepted_requests]), 200


@professional_bp.route('/service-requests/completed/<int:user_id>', methods=['GET'])
def get_completed_service_requests(user_id):
    professional = Professional.query.filter_by(user_id=user_id).first()
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404

    completed_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='completed').all()
    
    return jsonify([request.to_dict() for request in completed_requests]), 200




# Start service request
@professional_bp.route('/service-requests/<int:request_id>/start', methods=['PUT'])
def start_service_request(user, request_id):
    professional = user.professional_profile
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    # Only allow starting if assigned to this professional
    if service_request.professional_id != professional.id:
        return jsonify({'error': 'Service request is not assigned to you'}), 403
    
    if service_request.status != 'assigned':
        return jsonify({'error': 'Service request is not in assigned status'}), 400
    
    service_request.status = 'in_progress'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service request started successfully',
        'service_request': service_request.to_dict()
    }), 200

# Complete service request
from datetime import datetime

@professional_bp.route('/service-requests/<int:request_id>/complete/<int:user_id>', methods=['PUT'])
def complete_service_request(request_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    professional = user.professional_profile
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    # Only allow completing if assigned to this professional
    if service_request.professional_id != professional.id:
        return jsonify({'error': 'Service request is not assigned to you'}), 403
    
    if service_request.status != 'accepted':
        return jsonify({'error': 'Service request is not accepted'}), 400
    
    service_request.status = 'completed'
    service_request.date_of_completion = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service request completed successfully',
        'service_request': service_request.to_dict()
    }), 200



