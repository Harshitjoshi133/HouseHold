from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.customer_routes import customer_bp
from routes.professional_routes import professional_bp

__all__ = ['auth_bp', 'admin_bp', 'customer_bp', 'professional_bp']