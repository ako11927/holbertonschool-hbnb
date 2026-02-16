# HBnB Database - Quick Reference Guide

## 🔑 Quick Facts
- **Database**: `hbnb_db`
- **User**: `hbnb_user`
- **Password**: `hbnb_password_123`
- **Host**: `localhost`
- **Port**: 3306

## 📋 Table Summary
| Table | Primary Key | Records | Key Columns |
|-------|------------|---------|-------------|
| users | id (UUID) | 4 | email (unique), is_admin |
| places | id (UUID) | 4 | owner_id, city, price |
| reviews | id (UUID) | 6 | user_id, place_id, rating |
| amenities | id (UUID) | 9 | name |
| place_amenities | place_id+amenity_id | 18 | foreign keys only |

## ⚡ Essential Queries

### 1. Connect to Database
```bash
mysql -u hbnb_user -p'hbnb_password_123' -h localhost hbnb_db
2. List All Tables
sql
SHOW TABLES;
3. Check Table Structure
sql
DESCRIBE users;
-- or
SHOW CREATE TABLE users;
4. View All Data Counts
sql
SELECT 
    (SELECT COUNT(*) FROM users) as users,
    (SELECT COUNT(*) FROM places) as places,
    (SELECT COUNT(*) FROM reviews) as reviews,
    (SELECT COUNT(*) FROM amenities) as amenities,
    (SELECT COUNT(*) FROM place_amenities) as place_amenities;
🎯 Most Useful Queries
Find Places in a City
sql
SELECT title, address, price, max_guests
FROM places 
WHERE city = 'Miami'
ORDER BY price ASC;
Get Places with Specific Amenity
sql
SELECT p.title, p.city, p.price, p.max_guests
FROM places p
JOIN place_amenities pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE a.name = 'WiFi'
  AND p.max_guests >= 2;
Get User's Properties
sql
SELECT u.first_name, u.last_name, p.title, p.city, p.price
FROM users u
JOIN places p ON u.id = p.owner_id
WHERE u.id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
Get Reviews for a Place
sql
SELECT r.rating, LEFT(r.text, 100) as preview,
       CONCAT(u.first_name, ' ', u.last_name) as reviewer,
       r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = '123e4567-e89b-12d3-a456-426614174001'
ORDER BY r.created_at DESC;
🛠️ Admin Operations
Make User Admin
sql
UPDATE users 
SET is_admin = 1 
WHERE email = 'user@example.com';
List All Users (Admin View)
sql
SELECT id, first_name, last_name, email, 
       is_admin, created_at
FROM users
ORDER BY is_admin DESC, created_at DESC;
⚠️ Common Issues & Solutions
1. Connection Issues
bash
# Check if MySQL is running
sudo service mysql status

# Restart MySQL
sudo service mysql restart

# Test connection
mysql -u hbnb_user -p'hbnb_password_123' -h localhost -e 'SELECT 1'
2. Permission Issues
sql
-- As root user
GRANT ALL PRIVILEGES ON hbnb_db.* TO 'hbnb_user'@'localhost';
FLUSH PRIVILEGES;
3. UUID Generation
sql
-- Insert new record with UUID
INSERT INTO users (id, first_name, last_name, email, password)
VALUES (UUID(), 'New', 'User', 'new@example.com', 'hashed_pass');
