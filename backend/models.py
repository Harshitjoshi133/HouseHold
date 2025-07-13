from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # 'admin', 'customer', 'professional'
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    pin_code = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    customer_profile = db.relationship('Customer', backref='user', uselist=False, cascade='all, delete-orphan')
    professional_profile = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete-orphan')
    # Add this to the User model relationships
    admin_profile = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'password':self.password_hash,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'pin_code': self.pin_code,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Assuming db is already defined elsewhere
# db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    department = db.Column(db.String(100))
    access_level = db.Column(db.String(50))  # 'full', 'restricted', 'read-only'
    last_login = db.Column(db.DateTime)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'department': self.department,
            'access_level': self.access_level,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'user': self.user.to_dict() if self.user else None
        }


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    preferences = db.Column(db.Text)
    is_blocked = db.Column(db.Boolean, default=False)
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'preferences': self.preferences,
            'is_blocked':self.is_blocked,
            'user': self.user.to_dict() if self.user else None
        }

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    experience = db.Column(db.Integer)  # Years of experience
    description = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    document_path = db.Column(db.String(255))  # Path to verification document
    avg_rating = db.Column(db.Float, default=0.0)
    document_path = db.Column(db.String(255))
    
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'service_id': self.service_id,
            'experience': self.experience,
            'description': self.description,
            'is_verified': self.is_verified,
            'avg_rating': self.avg_rating,
            'document_path':self.document_path,
            'user': self.user.to_dict() if self.user else None,
            'service': self.service.to_dict() if self.service else None
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    price = db.Column(db.Float)
    time_required = db.Column(db.Integer)  # Time in hours
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    professionals = db.relationship('Professional', backref='service', lazy='dynamic')
    service_requests = db.relationship('ServiceRequest', backref='service', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'time_required': self.time_required,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='requested')  # 'requested', 'assigned', 'in_progress', 'completed', 'closed', 'rejected'
    remarks = db.Column(db.Text)
    address = db.Column(db.String(200))
    pin_code = db.Column(db.String(10))
    
    # Relationships
    reviews = db.relationship('Review', backref='service_request', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id,
            'date_of_request': self.date_of_request.isoformat(),
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'date_of_completion': self.date_of_completion.isoformat() if self.date_of_completion else None,
            'status': self.status,
            'remarks': self.remarks,
            'address': self.address,
            'pin_code': self.pin_code,
            'service': self.service.to_dict() if self.service else None
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'))
    rating = db.Column(db.Integer)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_request_id': self.service_request_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }