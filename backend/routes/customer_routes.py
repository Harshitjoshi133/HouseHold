from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from datetime import datetime

from models import db, User, Customer, Service, ServiceRequest, Review, Professional

customer_bp = Blueprint('customer', __name__)

# Middleware to check if user is a customer
def customer_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'customer':
            return jsonify({'error': 'Customer access required'}), 403
            
        return fn(user, *args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper

# Get available services

@customer_bp.route('/services', methods=['GET'])
def get_services():
    try:
    # Get query parameters
        search_term = request.args.get('search', '')
        pin_code = request.args.get('pin_code', '')
        category = request.args.get('category', '')

        query = Service.query

        # Filter by search term
        if search_term:
            query = query.filter(
                Service.name.ilike(f'%{search_term}%') | 
                Service.description.ilike(f'%{search_term}%')
            )

        # Filter by category
        if category:
            query = query.filter(Service.category == category)  # Assuming 'category' is a column in Service

        services = query.all()

        # Filter by pin_code if provided
        if pin_code:
            filtered_services = []
            for service in services:
                professionals = Professional.query.join(User).filter(
                    Professional.service_id == service.id,
                    Professional.is_verified == True,
                    User.pin_code == pin_code,
                    User.is_active == True
                ).all()
                if professionals:
                    filtered_services.append(service)
            
            services = filtered_services

        return jsonify({'services': [service.to_dict() for service in services]}), 200
    except Exception as e:
        return jsonify({'Error':(str(e))}),500


@customer_bp.route('/services/<int:service_id>', methods=['GET'])
def get_services_by_id(service_id):
    try:
    # Get query parameters
        query = Service.query

        if service_id:
            query = query.filter(Service.id == service_id)
        services = query.all()

        print(services)
        return jsonify({'services': [service.to_dict() for service in services]}), 200
    except Exception as e:
        return jsonify({'Error':(str(e))}),500


# Create service request
@customer_bp.route('/service-requests', methods=['POST'])
def create_service_request():
    data = request.json   
    # Validate service
    print(data)
    id = data.get('service_id')
    service = Service.query.get(id)
    user_id=data.get('user_id')
    print(user_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    # Parse scheduled date
    try:
        scheduled_date = datetime.fromisoformat(data.get('scheduled_date'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid scheduled date format'}), 400
    print(user_id)
    user=User.query.filter_by(id=user_id).first()
    print(user)
    professional_id=data.get("professional_id")
    # Create service request
    service_request = ServiceRequest(
        service_id=id,
        customer_id=user_id,
        address=user.address,
        scheduled_date=scheduled_date,
        professional_id=professional_id,
        status='requested',
        remarks=data.get('remarks', ''),
        pin_code=user.pin_code
    )

    db.session.add(service_request)
    db.session.commit()
    print(service_request.to_dict())
    return jsonify({
        'message': 'Service request created successfully',
        'service_request': service_request.to_dict()
    }), 201

# Get customer's service requests
@customer_bp.route('/service-requests/<int:user_id>', methods=['GET'])
def get_service_requests(user_id):
    user=User.query.filter_by(id=user_id).first()
    customer = Customer.query.filter_by(user_id=user.id).first()
    
    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404
    
    status_filter = request.args.get('status')
    
    query = ServiceRequest.query.filter_by(customer_id=user_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    service_requests = query.order_by(ServiceRequest.date_of_request.desc()).all()
    
    return jsonify([request.to_dict() for request in service_requests]), 200

# Update service request
@customer_bp.route('/service-requests/<int:request_id>', methods=['PUT'])
def update_service_request(request_id):
    data = request.json
    user_id=data.get('user_id')
    user=User.query.filter_by(id=user_id).first()
    customer = Customer.query.filter_by(user_id=user_id).first()
    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404
    
    service_request = ServiceRequest.query.filter_by(
        id=request_id, customer_id=customer.user_id
    ).first()
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    # Only allow updates if the request is not closed
    if service_request.status == 'closed':
        return jsonify({'error': 'Cannot update a closed service request'}), 400
    
    data = request.json
    
    # Update fields
    if 'scheduled_date' in data:
        try:
            service_request.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid scheduled date format'}), 400
    
    if 'remarks' in data:
        service_request.remarks = data['remarks']
    
    if 'status' in data and data['status'] == 'closed':
        # Only allow closing if the status is 'completed'
        if service_request.status != 'completed':
            return jsonify({'error': 'Cannot close a request that is not completed'}), 400
        
        service_request.status = 'closed'
        service_request.date_of_completion = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Service request updated successfully',
        'service_request': service_request.to_dict()
    }), 200

# Create review for a service request
@customer_bp.route('/service-requests/<int:request_id>/reviews', methods=['POST'])
def create_review(request_id):
    data = request.json
    print(data)
    user_id=data.get('user_id')
    user=User.query.filter_by(id=user_id).first()
    print(user_id)
    customer = Customer.query.filter_by(user_id=user_id).first()
    print(customer)
    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404
    print(request_id)
    service_request = ServiceRequest.query.filter_by(
        id=request_id, customer_id=user_id
    ).first()

    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    # Validate rating
    rating = data.get('rating')
    if rating is None or not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    # Validate comment
    comment = data.get('remark', '').strip()
    if not comment:
        return jsonify({'error': 'Review comment cannot be empty'}), 400

    # Create review
    review = Review(
        service_request_id=service_request.id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)

    # Update professional's average rating
    if service_request.professional_id:
        professional = Professional.query.get(service_request.professional_id)
        if professional:
            reviews = Review.query.join(ServiceRequest).filter(
                ServiceRequest.professional_id == professional.id
            ).all()
            total_rating = sum(r.rating for r in reviews) + rating
            professional.avg_rating = total_rating / (len(reviews) + 1)

    db.session.commit()

    return jsonify({
        'message': 'Review and rating stored successfully',
        'review': review.to_dict()
    }), 201

# Get professionals for a service
@customer_bp.route('/services/<int:service_id>/professionals', methods=['GET'])
def get_service_professionals(service_id):
    service = Service.query.get(service_id)
    print(service.id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    # ,
    #     
    professionals = Professional.query.filter_by(
        service_id=service_id,
        is_verified=True
    ).join(User).all()
    print(professionals)
    return jsonify({
        'professionals': [prof.to_dict() for prof in professionals]
    }), 200


@customer_bp.route("/service/requests/<int:customer_id>", methods=["GET"])
def get_customer_requests(customer_id):
    #customer_id=2
    requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    return jsonify([req.to_dict() for req in requests])