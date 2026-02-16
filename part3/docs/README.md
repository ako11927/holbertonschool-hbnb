# HBnB Database Documentation

## 📚 Contents
1. [Database Diagrams](./database_diagram.md) - Complete ER diagrams and schema visualization
2. [Quick Reference](./quick_reference.md) - Fast lookup for common queries
3. [Interactive Diagrams](./diagrams.html) - Viewable ER diagrams in browser
4. [Setup Summary](./SUMMARY.md) - Complete setup summary

## 🗄️ Database Overview
The HBnB database is a relational database designed for a vacation rental platform, featuring:

### Core Tables (5)
1. **users** - User accounts with authentication
2. **places** - Rental properties listings
3. **reviews** - User reviews and ratings
4. **amenities** - Property features and facilities
5. **place_amenities** - Many-to-many relationship table

### Key Features
- UUID primary keys for all tables
- Foreign key constraints with CASCADE DELETE
- Unique constraints on email and reviews
- Timestamp tracking (created_at, updated_at)
- Admin user system with RBAC support

## 📊 Current Statistics
| Table | Records | Description |
|-------|---------|-------------|
| Users | 4 | 1 admin + 3 regular users |
| Places | 4 | Sample rental properties |
| Reviews | 6 | User reviews and ratings |
| Amenities | 9 | Property features |
| Place_Amenities | 18 | Place-amenity associations |

## ✅ Verification Status
- **Schema**: ✓ Complete (5 tables)
- **Data**: ✓ Loaded (41 total records)
- **Constraints**: ✓ Working (foreign keys, unique)
- **Admin**: ✓ Present (admin@hbnb.io)
- **CRUD**: ✓ Tested (all operations working)

## 🚀 Quick Start

### 1. Connect to Database
```bash
mysql -u hbnb_user -p'hbnb_password_123' -h localhost hbnb_db
2. View Tables
sql
SHOW TABLES;
DESCRIBE users;  -- Or any table
3. View Diagrams
bash
# Open in browser
xdg-open docs/diagrams.html
4. Run Tests
bash
# Verify database
python3 sql/verify_database.py

# Run CRUD tests
mysql -u hbnb_user -p'hbnb_password_123' -h localhost hbnb_db < sql/test_crud_operations.sql
