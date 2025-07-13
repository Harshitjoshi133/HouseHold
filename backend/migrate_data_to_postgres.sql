-- Data Migration Script: SQLite to PostgreSQL
-- This script helps migrate existing data from SQLite to PostgreSQL
-- Run this after creating the database structure

-- Note: Replace the INSERT statements with your actual data from SQLite
-- You can export data from SQLite using: sqlite3 household_services.db ".dump"

-- Sample data migration (replace with your actual data)

-- Migrate users data
-- INSERT INTO users (id, username, email, password_hash, role, full_name, phone_number, address, pin_code, created_at, is_active) VALUES
-- (1, 'admin', 'admin@example.com', 'pbkdf2:sha256:600000$hash_here', 'admin', 'Administrator', NULL, NULL, NULL, '2024-01-01 00:00:00', TRUE),
-- (2, 'john_doe', 'john@example.com', 'pbkdf2:sha256:600000$hash_here', 'customer', 'John Doe', '+1234567890', '123 Main St', '12345', '2024-01-01 00:00:00', TRUE);

-- Migrate services data (if any exists)
-- INSERT INTO services (id, name, price, time_required, description, created_at) VALUES
-- (1, 'Plumbing', 50.00, 2, 'Fixing pipes and leaks', '2024-01-01 00:00:00'),
-- (2, 'Electrician', 40.00, 3, 'Wiring and electrical fixes', '2024-01-01 00:00:00');

-- Migrate admins data
-- INSERT INTO admins (id, user_id, department, access_level, last_login) VALUES
-- (1, 1, 'Management', 'full', NULL);

-- Migrate customers data
-- INSERT INTO customers (id, user_id, preferences, is_blocked) VALUES
-- (1, 2, 'Prefers morning appointments', FALSE);

-- Migrate professionals data
-- INSERT INTO professionals (id, user_id, service_id, experience, description, is_verified, document_path, avg_rating) VALUES
-- (1, 3, 1, 5, 'Experienced plumber with 5 years of experience', TRUE, '/uploads/documents/plumber_cert.pdf', 4.5);

-- Migrate service_requests data
-- INSERT INTO service_requests (id, service_id, customer_id, professional_id, date_of_request, scheduled_date, date_of_completion, status, remarks, address, pin_code) VALUES
-- (1, 1, 1, 1, '2024-01-01 10:00:00', '2024-01-02 14:00:00', NULL, 'assigned', 'Leaky faucet in kitchen', '123 Main St', '12345');

-- Migrate reviews data
-- INSERT INTO reviews (id, service_request_id, rating, comment, created_at) VALUES
-- (1, 1, 5, 'Excellent service, very professional', '2024-01-03 15:00:00');

-- Reset sequences to match the highest ID values
-- SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
-- SELECT setval('services_id_seq', (SELECT MAX(id) FROM services));
-- SELECT setval('admins_id_seq', (SELECT MAX(id) FROM admins));
-- SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));
-- SELECT setval('professionals_id_seq', (SELECT MAX(id) FROM professionals));
-- SELECT setval('service_requests_id_seq', (SELECT MAX(id) FROM service_requests));
-- SELECT setval('reviews_id_seq', (SELECT MAX(id) FROM reviews));

-- Verify data migration
-- SELECT 'users' as table_name, COUNT(*) as count FROM users
-- UNION ALL
-- SELECT 'services', COUNT(*) FROM services
-- UNION ALL
-- SELECT 'admins', COUNT(*) FROM admins
-- UNION ALL
-- SELECT 'customers', COUNT(*) FROM customers
-- UNION ALL
-- SELECT 'professionals', COUNT(*) FROM professionals
-- UNION ALL
-- SELECT 'service_requests', COUNT(*) FROM service_requests
-- UNION ALL
-- SELECT 'reviews', COUNT(*) FROM reviews; 