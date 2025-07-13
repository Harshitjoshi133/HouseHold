-- PostgreSQL Database Creation Script for Household Services
-- Generated from SQLite schema conversion
-- Compatible with Neon Database and other PostgreSQL providers

-- Create database (run this separately if needed)
-- CREATE DATABASE household_services;

-- Enable UUID extension (optional, for better ID management)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(128),
    role VARCHAR(20),
    full_name VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(200),
    pin_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create indexes for users table
CREATE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_role ON users (role);

-- Create services table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    time_required INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for services table
CREATE INDEX ix_services_name ON services (name);

-- Create admins table
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users (id) ON DELETE CASCADE,
    department VARCHAR(100),
    access_level VARCHAR(50),
    last_login TIMESTAMP
);

-- Create customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users (id) ON DELETE CASCADE,
    preferences TEXT,
    is_blocked BOOLEAN DEFAULT FALSE
);

-- Create professionals table
CREATE TABLE professionals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users (id) ON DELETE CASCADE,
    service_id INTEGER REFERENCES services (id) ON DELETE SET NULL,
    experience INTEGER,
    description TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    document_path VARCHAR(255),
    avg_rating DECIMAL(3,2) DEFAULT 0.0
);

-- Create service_requests table
CREATE TABLE service_requests (
    id SERIAL PRIMARY KEY,
    service_id INTEGER REFERENCES services (id) ON DELETE SET NULL,
    customer_id INTEGER REFERENCES customers (id) ON DELETE CASCADE,
    professional_id INTEGER REFERENCES professionals (id) ON DELETE SET NULL,
    date_of_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_date TIMESTAMP,
    date_of_completion TIMESTAMP,
    status VARCHAR(20) DEFAULT 'requested',
    remarks TEXT,
    address VARCHAR(200),
    pin_code VARCHAR(10)
);

-- Create reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    service_request_id INTEGER REFERENCES service_requests (id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX ix_service_requests_customer_id ON service_requests (customer_id);
CREATE INDEX ix_service_requests_professional_id ON service_requests (professional_id);
CREATE INDEX ix_service_requests_status ON service_requests (status);
CREATE INDEX ix_service_requests_date ON service_requests (date_of_request);
CREATE INDEX ix_reviews_service_request_id ON reviews (service_request_id);
CREATE INDEX ix_professionals_service_id ON professionals (service_id);
CREATE INDEX ix_professionals_verified ON professionals (is_verified);

-- Insert sample data (optional)
INSERT INTO services (name, price, time_required, description) VALUES
('Plumbing', 50.00, 2, 'Fixing pipes and leaks'),
('Electrician', 40.00, 3, 'Wiring and electrical fixes'),
('Cleaning', 30.00, 4, 'Home and office cleaning services'),
('Carpentry', 45.00, 3, 'Woodwork and furniture repair'),
('Painting', 35.00, 6, 'Interior and exterior painting');

-- Create admin user (optional)
INSERT INTO users (username, email, password_hash, role, full_name, is_active) VALUES
('admin', 'admin@example.com', 'pbkdf2:sha256:600000$your_hash_here', 'admin', 'Administrator', TRUE);

-- Grant permissions (run as superuser if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;

-- Create views for common queries (optional)
CREATE VIEW active_users AS
SELECT * FROM users WHERE is_active = TRUE;

CREATE VIEW verified_professionals AS
SELECT p.*, u.username, u.email, u.full_name, s.name as service_name
FROM professionals p
JOIN users u ON p.user_id = u.id
JOIN services s ON p.service_id = s.id
WHERE p.is_verified = TRUE;

CREATE VIEW service_request_summary AS
SELECT 
    sr.id,
    sr.status,
    sr.date_of_request,
    sr.scheduled_date,
    s.name as service_name,
    c.id as customer_id,
    cu.username as customer_username,
    p.id as professional_id,
    pu.username as professional_username
FROM service_requests sr
JOIN services s ON sr.service_id = s.id
JOIN customers c ON sr.customer_id = c.id
JOIN users cu ON c.user_id = cu.id
LEFT JOIN professionals p ON sr.professional_id = p.id
LEFT JOIN users pu ON p.user_id = pu.id;

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts for the household services platform';
COMMENT ON TABLE services IS 'Available services offered by professionals';
COMMENT ON TABLE admins IS 'Administrator user profiles';
COMMENT ON TABLE customers IS 'Customer user profiles';
COMMENT ON TABLE professionals IS 'Professional service providers';
COMMENT ON TABLE service_requests IS 'Service requests made by customers';
COMMENT ON TABLE reviews IS 'Reviews and ratings for completed services'; 