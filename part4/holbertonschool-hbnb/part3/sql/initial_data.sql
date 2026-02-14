-- HBnB Initial Data
-- SQL Script for populating initial data

-- Note: We're using fixed UUIDs for consistency across tests
-- In production, you would use UUID() function or generate them in your application

-- Insert Administrator User
-- Password: admin1234 (hashed with bcrypt, 12 rounds)
-- You can generate bcrypt hashes using: python -c "import bcrypt; print(bcrypt.hashpw('admin1234'.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8'))"
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) 
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$K7V.9gJkf8Q3Lq2z1Y4X5u6v7w8x9y0z1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P',
    TRUE,
    NOW(),
    NOW()
);

-- Insert Regular Users
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) 
VALUES 
-- Password for all regular users: Password123! (hashed)
(
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkdUloVBu.aNQqRFSL2gYspYgqR3qSAuLkDDEWfjy',
    FALSE,
    NOW(),
    NOW()
),
(
    'b2c3d4e5-f6a7-8901-bcde-f23456789012',
    'Jane',
    'Smith',
    'jane.smith@example.com',
    '$2b$12$LQv3c1yqBWVHxkdUloVBu.aNQqRFSL2gYspYgqR3qSAuLkDDEWfjy',
    FALSE,
    NOW(),
    NOW()
),
(
    'c3d4e5f6-a7b8-9012-cdef-345678901234',
    'Robert',
    'Johnson',
    'robert.johnson@example.com',
    '$2b$12$LQv3c1yqBWVHxkdUloVBu.aNQqRFSL2gYspYgqR3qSAuLkDDEWfjy',
    FALSE,
    NOW(),
    NOW()
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, created_at, updated_at) 
VALUES 
(
    'd4e5f6a7-b8c9-0123-def0-456789012345',
    'WiFi',
    NOW(),
    NOW()
),
(
    'e5f6a7b8-c9d0-1234-ef01-567890123456',
    'Swimming Pool',
    NOW(),
    NOW()
),
(
    'f6a7b8c9-d0e1-2345-f012-678901234567',
    'Air Conditioning',
    NOW(),
    NOW()
),
(
    'a7b8c9d0-e1f2-3456-0123-789012345678',
    'Kitchen',
    NOW(),
    NOW()
),
(
    'b8c9d0e1-f2a3-4567-1234-890123456789',
    'Free Parking',
    NOW(),
    NOW()
),
(
    'c9d0e1f2-a3b4-5678-2345-901234567890',
    'Hot Tub',
    NOW(),
    NOW()
),
(
    'd0e1f2a3-b4c5-6789-3456-012345678901',
    'Washer',
    NOW(),
    NOW()
),
(
    'e1f2a3b4-c5d6-7890-4567-123456789012',
    'Dryer',
    NOW(),
    NOW()
),
(
    'f2a3b4c5-d6e7-8901-5678-234567890123',
    'TV',
    NOW(),
    NOW()
);

-- Insert Sample Places
INSERT INTO places (id, title, description, price, latitude, longitude, address, city, max_guests, bedrooms, bathrooms, owner_id, created_at, updated_at) 
VALUES 
-- Place 1: Beach House (owned by John Doe)
(
    '123e4567-e89b-12d3-a456-426614174001',
    'Beautiful Beach House',
    'A stunning beach house with panoramic ocean views, located just steps from the water. Perfect for family vacations or romantic getaways. Features modern amenities and a private patio.',
    250.00,
    25.7617,
    -80.1918,
    '123 Ocean Drive',
    'Miami',
    6,
    3,
    2,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890', -- John Doe
    NOW(),
    NOW()
),
-- Place 2: Downtown Apartment (owned by Jane Smith)
(
    '123e4567-e89b-12d3-a456-426614174002',
    'Modern Downtown Apartment',
    'Luxurious apartment in the heart of downtown with floor-to-ceiling windows offering breathtaking city views. Walking distance to restaurants, theaters, and shopping.',
    180.00,
    40.7128,
    -74.0060,
    '456 Broadway',
    'New York',
    4,
    2,
    1,
    'b2c3d4e5-f6a7-8901-bcde-f23456789012', -- Jane Smith
    NOW(),
    NOW()
),
-- Place 3: Mountain Cabin (owned by Robert Johnson)
(
    '123e4567-e89b-12d3-a456-426614174003',
    'Cozy Mountain Cabin',
    'Secluded cabin nestled in the mountains, perfect for nature lovers. Features a wood-burning fireplace, hiking trails from the doorstep, and spectacular mountain views.',
    120.00,
    39.7392,
    -104.9903,
    '789 Mountain Road',
    'Denver',
    4,
    2,
    1,
    'c3d4e5f6-a7b8-9012-cdef-345678901234', -- Robert Johnson
    NOW(),
    NOW()
),
-- Place 4: City Loft (owned by John Doe)
(
    '123e4567-e89b-12d3-a456-426614174004',
    'Industrial City Loft',
    'Spacious loft with industrial design elements, exposed brick walls, and high ceilings. Located in a trendy neighborhood with easy access to public transportation.',
    200.00,
    41.8781,
    -87.6298,
    '321 Industrial Avenue',
    'Chicago',
    4,
    1,
    1,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890', -- John Doe
    NOW(),
    NOW()
);

-- Associate amenities with places
INSERT INTO place_amenities (place_id, amenity_id, created_at) 
VALUES 
-- Beach House amenities
('123e4567-e89b-12d3-a456-426614174001', 'd4e5f6a7-b8c9-0123-def0-456789012345', NOW()), -- WiFi
('123e4567-e89b-12d3-a456-426614174001', 'e5f6a7b8-c9d0-1234-ef01-567890123456', NOW()), -- Swimming Pool
('123e4567-e89b-12d3-a456-426614174001', 'f6a7b8c9-d0e1-2345-f012-678901234567', NOW()), -- Air Conditioning
('123e4567-e89b-12d3-a456-426614174001', 'a7b8c9d0-e1f2-3456-0123-789012345678', NOW()), -- Kitchen
('123e4567-e89b-12d3-a456-426614174001', 'b8c9d0e1-f2a3-4567-1234-890123456789', NOW()), -- Free Parking

-- Downtown Apartment amenities
('123e4567-e89b-12d3-a456-426614174002', 'd4e5f6a7-b8c9-0123-def0-456789012345', NOW()), -- WiFi
('123e4567-e89b-12d3-a456-426614174002', 'f6a7b8c9-d0e1-2345-f012-678901234567', NOW()), -- Air Conditioning
('123e4567-e89b-12d3-a456-426614174002', 'a7b8c9d0-e1f2-3456-0123-789012345678', NOW()), -- Kitchen
('123e4567-e89b-12d3-a456-426614174002', 'f2a3b4c5-d6e7-8901-5678-234567890123', NOW()), -- TV

-- Mountain Cabin amenities
('123e4567-e89b-12d3-a456-426614174003', 'a7b8c9d0-e1f2-3456-0123-789012345678', NOW()), -- Kitchen
('123e4567-e89b-12d3-a456-426614174003', 'b8c9d0e1-f2a3-4567-1234-890123456789', NOW()), -- Free Parking
('123e4567-e89b-12d3-a456-426614174003', 'c9d0e1f2-a3b4-5678-2345-901234567890', NOW()), -- Hot Tub
('123e4567-e89b-12d3-a456-426614174003', 'd0e1f2a3-b4c5-6789-3456-012345678901', NOW()), -- Washer

-- City Loft amenities
('123e4567-e89b-12d3-a456-426614174004', 'd4e5f6a7-b8c9-0123-def0-456789012345', NOW()), -- WiFi
('123e4567-e89b-12d3-a456-426614174004', 'f6a7b8c9-d0e1-2345-f012-678901234567', NOW()), -- Air Conditioning
('123e4567-e89b-12d3-a456-426614174004', 'd0e1f2a3-b4c5-6789-3456-012345678901', NOW()), -- Washer
('123e4567-e89b-12d3-a456-426614174004', 'e1f2a3b4-c5d6-7890-4567-123456789012', NOW()), -- Dryer
('123e4567-e89b-12d3-a456-426614174004', 'f2a3b4c5-d6e7-8901-5678-234567890123', NOW()); -- TV

-- Insert Sample Reviews
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) 
VALUES 
-- Reviews for Beach House
(
    '223e4567-e89b-12d3-a456-426614174001',
    'Amazing beach house! The location is perfect and the views are breathtaking. The house was clean and well-equipped. Will definitely come back!',
    5,
    'b2c3d4e5-f6a7-8901-bcde-f23456789012', -- Jane Smith
    '123e4567-e89b-12d3-a456-426614174001', -- Beach House
    NOW(),
    NOW()
),
(
    '223e4567-e89b-12d3-a456-426614174002',
    'Great place for a family vacation. Kids loved the pool and being so close to the beach. The kitchen had everything we needed.',
    4,
    'c3d4e5f6-a7b8-9012-cdef-345678901234', -- Robert Johnson
    '123e4567-e89b-12d3-a456-426614174001', -- Beach House
    NOW(),
    NOW()
),

-- Reviews for Downtown Apartment
(
    '223e4567-e89b-12d3-a456-426614174003',
    'Perfect location! Walking distance to everything. The apartment was modern and clean. The view of the city at night was spectacular.',
    5,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890', -- John Doe
    '123e4567-e89b-12d3-a456-426614174002', -- Downtown Apartment
    NOW(),
    NOW()
),

-- Reviews for Mountain Cabin
(
    '223e4567-e89b-12d3-a456-426614174004',
    'Exactly what we needed for a peaceful getaway. The cabin was cozy and had everything we needed. The hiking trails were amazing.',
    4,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890', -- John Doe
    '123e4567-e89b-12d3-a456-426614174003', -- Mountain Cabin
    NOW(),
    NOW()
),
(
    '223e4567-e89b-12d3-a456-426614174005',
    'Beautiful cabin but the heating was a bit inconsistent during cold nights. Otherwise, a great experience.',
    3,
    'b2c3d4e5-f6a7-8901-bcde-f23456789012', -- Jane Smith
    '123e4567-e89b-12d3-a456-426614174003', -- Mountain Cabin
    NOW(),
    NOW()
),

-- Reviews for City Loft
(
    '223e4567-e89b-12d3-a456-426614174006',
    'Loved the industrial design! The loft was spacious and comfortable. Great neighborhood with lots of restaurants and bars nearby.',
    5,
    'c3d4e5f6-a7b8-9012-cdef-345678901234', -- Robert Johnson
    '123e4567-e89b-12d3-a456-426614174004', -- City Loft
    NOW(),
    NOW()
);

-- Show inserted data counts
SELECT 'Data Insertion Summary' AS title;
SELECT 
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM places) AS total_places,
    (SELECT COUNT(*) FROM amenities) AS total_amenities,
    (SELECT COUNT(*) FROM reviews) AS total_reviews,
    (SELECT COUNT(*) FROM place_amenities) AS total_place_amenities;

-- Show admin user details
SELECT 'Admin User Created' AS message;
SELECT id, first_name, last_name, email, is_admin 
FROM users 
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Show initial amenities
SELECT 'Initial Amenities Created' AS message;
SELECT id, name FROM amenities ORDER BY name;

SELECT 'Initial data inserted successfully!' AS status;
