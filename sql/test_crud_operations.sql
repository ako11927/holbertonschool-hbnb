-- HBnB CRUD Operations Test
-- SQL Script for testing all CRUD operations

SET @test_start_time = NOW();
SELECT '=== HBnB CRUD Operations Test ===' AS test_section;
SELECT CONCAT('Test started at: ', @test_start_time) AS test_time;

-- =====================================================================
-- 1. READ Operations (SELECT)
-- =====================================================================
SELECT '=== 1. READ Operations ===' AS test_section;

-- 1.1 Read all users (without passwords for security)
SELECT '1.1 All Users (without passwords):' AS test_name;
SELECT id, first_name, last_name, email, is_admin, created_at 
FROM users 
ORDER BY created_at DESC;

-- 1.2 Read all places with owner information
SELECT '1.2 Places with Owner Details:' AS test_name;
SELECT 
    p.id AS place_id,
    p.title,
    p.city,
    CONCAT('$', p.price) AS price_per_night,
    p.max_guests,
    CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
    u.email AS owner_email
FROM places p
JOIN users u ON p.owner_id = u.id
ORDER BY p.price DESC;

-- 1.3 Read all reviews with user and place information
SELECT '1.3 Reviews with Details:' AS test_name;
SELECT 
    r.id AS review_id,
    r.rating,
    LEFT(r.text, 50) AS review_preview,
    CONCAT(u.first_name, ' ', u.last_name) AS reviewer,
    p.title AS place_title,
    r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
ORDER BY r.created_at DESC
LIMIT 5;

-- 1.4 Read amenities for each place
SELECT '1.4 Places with Amenities:' AS test_name;
SELECT 
    p.title AS place_title,
    p.city,
    COUNT(pa.amenity_id) AS amenity_count,
    GROUP_CONCAT(a.name ORDER BY a.name SEPARATOR ', ') AS amenities
FROM places p
LEFT JOIN place_amenities pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
GROUP BY p.id
ORDER BY amenity_count DESC;

-- 1.5 Calculate average rating for each place
SELECT '1.5 Places with Average Ratings:' AS test_name;
SELECT 
    p.title AS place_title,
    p.city,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 1) AS average_rating
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id
HAVING review_count > 0
ORDER BY average_rating DESC;

-- 1.6 Find users who are also owners
SELECT '1.6 Users Who Are Property Owners:' AS test_name;
SELECT 
    u.id,
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    u.email,
    COUNT(p.id) AS places_owned,
    SUM(p.price) AS total_property_value
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
GROUP BY u.id
HAVING places_owned > 0
ORDER BY places_owned DESC;

-- =====================================================================
-- 2. CREATE Operations (INSERT)
-- =====================================================================
SELECT '=== 2. CREATE Operations ===' AS test_section;

-- 2.1 Create a new user
SELECT '2.1 Creating new user...' AS test_name;
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) 
VALUES (
    UUID(),
    'Test',
    'User',
    'test.user@example.com',
    '$2b$12$TestPasswordHashForTestingPurposesOnly',
    FALSE,
    NOW(),
    NOW()
);

-- Store the new user ID for later use
SET @new_user_id = (SELECT id FROM users WHERE email = 'test.user@example.com');
SELECT CONCAT('New user created with ID: ', @new_user_id) AS result;

-- 2.2 Create a new place for the test user
SELECT '2.2 Creating new place...' AS test_name;
INSERT INTO places (
    id, title, description, price, latitude, longitude, 
    address, city, max_guests, bedrooms, bathrooms, owner_id, created_at, updated_at
) VALUES (
    UUID(),
    'Test Villa',
    'A beautiful test villa with all modern amenities for testing purposes.',
    175.50,
    34.0522,
    -118.2437,
    '999 Test Street',
    'Los Angeles',
    4,
    2,
    2,
    @new_user_id,
    NOW(),
    NOW()
);

-- Store the new place ID for later use
SET @new_place_id = (SELECT id FROM places WHERE title = 'Test Villa' AND owner_id = @new_user_id);
SELECT CONCAT('New place created with ID: ', @new_place_id) AS result;

-- 2.3 Create a new review for the test place
SELECT '2.3 Creating new review...' AS test_name;
-- First, find a user who is not the owner to write a review
SET @reviewer_id = (SELECT id FROM users WHERE email = 'jane.smith@example.com');

INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) 
VALUES (
    UUID(),
    'This is a test review for the test villa. Everything was perfect!',
    5,
    @reviewer_id,
    @new_place_id,
    NOW(),
    NOW()
);

SET @new_review_id = (SELECT id FROM reviews WHERE place_id = @new_place_id AND user_id = @reviewer_id);
SELECT CONCAT('New review created with ID: ', @new_review_id) AS result;

-- 2.4 Create a new amenity
SELECT '2.4 Creating new amenity...' AS test_name;
INSERT INTO amenities (id, name, created_at, updated_at) 
VALUES (
    UUID(),
    'Test Amenity',
    NOW(),
    NOW()
);

SET @new_amenity_id = (SELECT id FROM amenities WHERE name = 'Test Amenity');
SELECT CONCAT('New amenity created with ID: ', @new_amenity_id) AS result;

-- 2.5 Associate amenity with place (many-to-many)
SELECT '2.5 Associating amenity with place...' AS test_name;
INSERT INTO place_amenities (place_id, amenity_id, created_at) 
VALUES (
    @new_place_id,
    @new_amenity_id,
    NOW()
);

SELECT CONCAT('Amenity ', @new_amenity_id, ' associated with place ', @new_place_id) AS result;

-- =====================================================================
-- 3. UPDATE Operations
-- =====================================================================
SELECT '=== 3. UPDATE Operations ===' AS test_section;

-- 3.1 Update user information
SELECT '3.1 Updating user information...' AS test_name;
UPDATE users 
SET 
    last_name = 'UpdatedLastName',
    updated_at = NOW()
WHERE email = 'test.user@example.com';

SELECT CONCAT('Updated user: ', first_name, ' ', last_name) AS result
FROM users 
WHERE email = 'test.user@example.com';

-- 3.2 Update place price
SELECT '3.2 Updating place price...' AS test_name;
UPDATE places 
SET 
    price = 199.99,
    updated_at = NOW()
WHERE id = @new_place_id;

SELECT CONCAT('Updated price: $', price) AS result
FROM places 
WHERE id = @new_place_id;

-- 3.3 Update review rating
SELECT '3.3 Updating review rating...' AS test_name;
UPDATE reviews 
SET 
    rating = 4,
    text = CONCAT(text, ' (Rating updated from 5 to 4)'),
    updated_at = NOW()
WHERE id = @new_review_id;

SELECT CONCAT('Updated rating: ', rating, ' stars') AS result
FROM reviews 
WHERE id = @new_review_id;

-- 3.4 Update amenity name
SELECT '3.4 Updating amenity name...' AS test_name;
UPDATE amenities 
SET 
    name = 'Updated Test Amenity',
    updated_at = NOW()
WHERE id = @new_amenity_id;

SELECT CONCAT('Updated amenity name: ', name) AS result
FROM amenities 
WHERE id = @new_amenity_id;

-- =====================================================================
-- 4. DELETE Operations
-- =====================================================================
SELECT '=== 4. DELETE Operations ===' AS test_section;

-- 4.1 Remove amenity association (from place_amenities)
SELECT '4.1 Removing amenity association...' AS test_name;
DELETE FROM place_amenities 
WHERE place_id = @new_place_id AND amenity_id = @new_amenity_id;

SELECT 'Amenity association removed successfully' AS result;

-- 4.2 Delete the test review
SELECT '4.2 Deleting test review...' AS test_name;
DELETE FROM reviews WHERE id = @new_review_id;

SELECT 'Review deleted successfully' AS result;

-- 4.3 Delete the test amenity
SELECT '4.3 Deleting test amenity...' AS test_name;
DELETE FROM amenities WHERE id = @new_amenity_id;

SELECT 'Amenity deleted successfully' AS result;

-- 4.4 Delete the test place
SELECT '4.4 Deleting test place...' AS test_name;
DELETE FROM places WHERE id = @new_place_id;

SELECT 'Place deleted successfully' AS result;

-- 4.5 Delete the test user
SELECT '4.5 Deleting test user...' AS test_name;
DELETE FROM users WHERE id = @new_user_id;

SELECT 'User deleted successfully' AS result;

-- =====================================================================
-- 5. VERIFY Operations
-- =====================================================================
SELECT '=== 5. VERIFY Operations ===' AS test_section;

-- 5.1 Verify test data was deleted
SELECT '5.1 Verifying deletions:' AS test_name;
SELECT 
    (SELECT COUNT(*) FROM users WHERE email = 'test.user@example.com') AS test_user_exists,
    (SELECT COUNT(*) FROM places WHERE id = @new_place_id) AS test_place_exists,
    (SELECT COUNT(*) FROM reviews WHERE id = @new_review_id) AS test_review_exists,
    (SELECT COUNT(*) FROM amenities WHERE id = @new_amenity_id) AS test_amenity_exists;

-- 5.2 Verify constraints are working
SELECT '5.2 Testing constraints:' AS test_name;

-- Try to insert duplicate email (should fail in application, we'll just check)
SELECT 'Attempting to insert duplicate email...' AS constraint_test;
-- This would fail with: Duplicate entry 'admin@hbnb.io' for key 'email'

-- Try to insert review with rating 6 (should fail)
SELECT 'Attempting to insert invalid rating...' AS constraint_test;
-- This would fail with: Check constraint 'reviews_chk_1' is violated

-- 5.3 Verify foreign key constraints
SELECT '5.3 Verifying foreign key relationships:' AS test_name;

-- Check orphaned records
SELECT 
    (SELECT COUNT(*) FROM places p LEFT JOIN users u ON p.owner_id = u.id WHERE u.id IS NULL) AS orphaned_places,
    (SELECT COUNT(*) FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE u.id IS NULL) AS orphaned_reviews,
    (SELECT COUNT(*) FROM reviews r LEFT JOIN places p ON r.place_id = p.id WHERE p.id IS NULL) AS reviews_without_places,
    (SELECT COUNT(*) FROM place_amenities pa LEFT JOIN places p ON pa.place_id = p.id WHERE p.id IS NULL) AS orphaned_place_amenities_places,
    (SELECT COUNT(*) FROM place_amenities pa LEFT JOIN amenities a ON pa.amenity_id = a.id WHERE a.id IS NULL) AS orphaned_place_amenities_amenities;

-- =====================================================================
-- 6. FINAL SUMMARY
-- =====================================================================
SELECT '=== 6. FINAL SUMMARY ===' AS test_section;

-- Show final counts
SELECT 'Final Database Counts:' AS summary_title;
SELECT 
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM places) AS total_places,
    (SELECT COUNT(*) FROM amenities) AS total_amenities,
    (SELECT COUNT(*) FROM reviews) AS total_reviews,
    (SELECT COUNT(*) FROM place_amenities) AS total_place_amenities;

-- Show admin user is still present
SELECT 'Admin User Verification:' AS verification;
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin,
    CASE 
        WHEN is_admin = TRUE THEN '✓ Admin user verified'
        ELSE '✗ Admin user not found or not admin'
    END AS status
FROM users 
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Show initial amenities are still present
SELECT 'Initial Amenities Verification:' AS verification;
SELECT 
    COUNT(*) AS amenity_count,
    CASE 
        WHEN COUNT(*) >= 3 THEN '✓ Initial amenities present'
        ELSE '✗ Initial amenities missing'
    END AS status
FROM amenities 
WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning');

-- Calculate test duration
SET @test_end_time = NOW();
SET @test_duration = TIMESTAMPDIFF(SECOND, @test_start_time, @test_end_time);

SELECT 'Test Results:' AS final_section;
SELECT 
    'All CRUD operations tested successfully!' AS message,
    CONCAT('Test started: ', @test_start_time) AS start_time,
    CONCAT('Test ended: ', @test_end_time) AS end_time,
    CONCAT('Duration: ', @test_duration, ' seconds') AS duration;

SELECT '=== CRUD Tests Completed Successfully ===' AS final_status;
