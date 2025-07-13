from flask import Flask,jsonify,send_from_directory,make_response, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from celery import Celery
import redis
import traceback
from datetime import datetime

from config import config
from models import db
from logger import setup_logger, log_error_with_context, log_api_request, log_security_event

# Initialize logger
logger = setup_logger()

# Initialize extensions
jwt = JWTManager()
celery = Celery(__name__)
migrate = Migrate()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    try:
        logger.info("Starting application initialization...")
        
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        app.config["JWT_VERIFY_SUB"]=False
        
        # Apply middleware
        app.wsgi_app = ProxyFix(app.wsgi_app)
        
        # Initialize CORS
        CORS(app, resources={r"/api/*": {"origins": "*"}})
        logger.info("CORS initialized successfully")
        
        # Initialize database
        db.init_app(app)
        migrate.init_app(app, db)
        logger.info("Database and migrations initialized successfully")
        
        # Initialize JWT
        jwt.init_app(app)
        logger.info("JWT initialized successfully")
        
        # Initialize Redis
        try:
            app.redis = redis.from_url(app.config['REDIS_URL'])
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            app.redis = None
        
        # Initialize Celery
        celery.conf.update(app.config)
        
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
        logger.info("Celery initialized successfully")
        
        # Register blueprints
        try:
            from routes.auth_routes import auth_bp
            from routes.admin_routes import admin_bp
            from routes.customer_routes import customer_bp
            from routes.professional_routes import professional_bp
            
            app.register_blueprint(auth_bp, url_prefix='/api/auth')
            app.register_blueprint(admin_bp, url_prefix='/api/admin')
            app.register_blueprint(customer_bp, url_prefix='/api/customer')
            app.register_blueprint(professional_bp, url_prefix='/api/professional')
            
            logger.info("All blueprints registered successfully")
        except Exception as e:
            logger.error(f"Failed to register blueprints: {e}")
            log_error_with_context(e, {"stage": "blueprint_registration"})
        
        # Create database tables
        try:
            with app.app_context():
                db.create_all()
                _create_admin_user()
            logger.info("Database tables created and admin user initialized")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            log_error_with_context(e, {"stage": "database_initialization"})
        
        # Register error handlers
        register_error_handlers(app)
        
        logger.info("Application initialization completed successfully")
        return app
        
    except Exception as e:
        logger.critical(f"Failed to create application: {e}")
        log_error_with_context(e, {"stage": "application_creation"})
        raise

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {request.url} - {error}")
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be processed',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"Unauthorized access: {request.url}")
        log_security_event("unauthorized_access", f"Attempted access to {request.url}", "WARNING")
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"Forbidden access: {request.url}")
        log_security_event("forbidden_access", f"Attempted access to {request.url}", "WARNING")
        return jsonify({
            'error': 'Forbidden',
            'message': 'Access denied',
            'timestamp': datetime.now().isoformat()
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        logger.info(f"Page not found: {request.url}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'timestamp': datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        log_error_with_context(error, {
            "url": request.url,
            "method": request.method,
            "user_agent": request.headers.get('User-Agent'),
            "ip": request.remote_addr
        })
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {error}")
        log_error_with_context(error, {
            "url": request.url,
            "method": request.method,
            "user_agent": request.headers.get('User-Agent'),
            "ip": request.remote_addr
        })
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500

def _create_admin_user():
    """Create admin user if not exists"""
    try:
        from models import User
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin',
                full_name='Administrator'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")
        log_error_with_context(e, {"stage": "admin_user_creation"})

# Create application instance
try:
    app = create_app()
    logger.info("Flask application created successfully")
except Exception as e:
    logger.critical(f"Failed to create Flask application: {e}")
    log_error_with_context(e, {"stage": "app_creation"})
    raise

services = [
    {"id": 1, "name": "Plumbing", "price": 50, "description": "Fixing pipes and leaks"},
    {"id": 2, "name": "Electrician", "price": 40, "description": "Wiring and electrical fixes"},
    {"id": 3, "name": "Cleaning", "price": 30, "description": "Home and office cleaning services"}
]

# ✅ API route for fetching services
@app.route('/api/services', methods=['GET'])
@log_api_request
def get_services():
    """Get list of available services"""
    try:
        logger.info("Services API called")
        return jsonify(services)
    except Exception as e:
        logger.error(f"Error in get_services: {e}")
        log_error_with_context(e, {"endpoint": "/api/services", "method": "GET"})
        return jsonify({
            'error': 'Failed to fetch services',
            'message': 'An error occurred while fetching services'
        }), 500

@app.route('/uploads/<filename>')
def get_upload(filename):
    """Serve uploaded files"""
    try:
        logger.info(f"File upload requested: {filename}")
        response = make_response(send_from_directory('static/uploads', filename))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        return response
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        log_error_with_context(e, {"filename": filename, "endpoint": "/uploads/<filename>"})
        return jsonify({
            'error': 'File not found',
            'message': 'The requested file was not found'
        }), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "healthy"
        try:
            db.session.execute("SELECT 1")
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
            logger.warning(f"Database health check failed: {e}")
        
        # Check Redis connection
        redis_status = "healthy"
        if app.redis:
            try:
                app.redis.ping()
            except Exception as e:
                redis_status = f"unhealthy: {str(e)}"
                logger.warning(f"Redis health check failed: {e}")
        else:
            redis_status = "not configured"
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': db_status,
            'redis': redis_status,
            'version': '1.0.0'
        }
        
        # Overall status
        if db_status != "healthy" or (redis_status != "healthy" and redis_status != "not configured"):
            health_data['status'] = 'degraded'
            return jsonify(health_data), 503
        
        logger.info("Health check completed successfully")
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        log_error_with_context(e, {"endpoint": "/health"})
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask development server...")
        app.run(debug=True)
    except Exception as e:
        logger.critical(f"Failed to start Flask server: {e}")
        log_error_with_context(e, {"stage": "server_startup"})
        raise