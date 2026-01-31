#!/usr/bin/env python3
"""Verify HBnB database setup."""

import mysql.connector
import sys
import os
from datetime import datetime

class DatabaseVerifier:
    def __init__(self, host='localhost', database='hbnb_db', 
                 username='hbnb_user', password='hbnb_password_123'):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        
    def connect(self):
        """Connect to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password
            )
            print(f"✓ Connected to database: {self.database}")
            return True
        except mysql.connector.Error as err:
            print(f"✗ Connection failed: {err}")
            return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.connection:
            self.connection.close()
            print("✓ Disconnected from database")
    
    def check_tables(self):
        """Check if all required tables exist."""
        required_tables = ['users', 'places', 'amenities', 'reviews', 'place_amenities']
        existing_tables = []
        
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            existing_tables.append(table[0])
        
        print("\nChecking tables:")
        print("-" * 40)
        
        all_tables_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} (MISSING)")
                all_tables_exist = False
        
        return all_tables_exist
    
    def check_table_structure(self, table_name):
        """Check structure of a specific table."""
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        
        print(f"\n{table_name} table structure:")
        print("-" * 40)
        for column in columns:
            print(f"  {column[0]:20} {column[1]:20} {column[2]}")
    
    def check_data_counts(self):
        """Check data counts in all tables."""
        cursor = self.connection.cursor()
        
        queries = {
            'users': "SELECT COUNT(*) FROM users",
            'places': "SELECT COUNT(*) FROM places",
            'amenities': "SELECT COUNT(*) FROM amenities",
            'reviews': "SELECT COUNT(*) FROM reviews",
            'place_amenities': "SELECT COUNT(*) FROM place_amenities"
        }
        
        print("\nData counts:")
        print("-" * 40)
        
        for table, query in queries.items():
            cursor.execute(query)
            count = cursor.fetchone()[0]
            print(f"  {table:20} {count:4} records")
    
    def verify_admin_user(self):
        """Verify admin user exists and is admin."""
        cursor = self.connection.cursor()
        
        # Check admin user
        admin_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
        cursor.execute("""
            SELECT first_name, last_name, email, is_admin 
            FROM users 
            WHERE id = %s
        """, (admin_id,))
        
        admin = cursor.fetchone()
        
        print("\nAdmin user verification:")
        print("-" * 40)
        
        if admin:
            print(f"  ✓ Admin user found:")
            print(f"     Name:  {admin[0]} {admin[1]}")
            print(f"     Email: {admin[2]}")
            print(f"     Is Admin: {'Yes' if admin[3] else 'No'}")
            return admin[3]  # Return is_admin status
        else:
            print("  ✗ Admin user not found!")
            return False
    
    def verify_initial_amenities(self):
        """Verify initial amenities are present."""
        cursor = self.connection.cursor()
        
        initial_amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
        placeholders = ', '.join(['%s'] * len(initial_amenities))
        
        cursor.execute(f"""
            SELECT name 
            FROM amenities 
            WHERE name IN ({placeholders})
        """, tuple(initial_amenities))
        
        found_amenities = [row[0] for row in cursor.fetchall()]
        
        print("\nInitial amenities verification:")
        print("-" * 40)
        
        for amenity in initial_amenities:
            if amenity in found_amenities:
                print(f"  ✓ {amenity}")
            else:
                print(f"  ✗ {amenity} (MISSING)")
        
        return len(found_amenities) == len(initial_amenities)
    
    def test_foreign_key_constraints(self):
        """Test foreign key constraints."""
        cursor = self.connection.cursor()
        
        print("\nForeign key constraints test:")
        print("-" * 40)
        
        # Test 1: Try to insert a place with non-existent user
        try:
            cursor.execute("""
                INSERT INTO places (id, title, description, price, address, city, owner_id)
                VALUES (UUID(), 'Test', 'Test', 100, 'Test', 'Test', 'non-existent-id')
            """)
            print("  ✗ Should have failed: Invalid owner_id accepted")
            self.connection.rollback()
            return False
        except mysql.connector.Error:
            print("  ✓ Valid: Foreign key constraint works (invalid owner_id rejected)")
            self.connection.rollback()
        
        # Test 2: Try to insert duplicate user-place review
        cursor.execute("SELECT user_id, place_id FROM reviews LIMIT 1")
        existing_review = cursor.fetchone()
        
        if existing_review:
            try:
                cursor.execute("""
                    INSERT INTO reviews (id, text, rating, user_id, place_id)
                    VALUES (UUID(), 'Duplicate', 5, %s, %s)
                """, existing_review)
                print("  ✗ Should have failed: Duplicate review accepted")
                self.connection.rollback()
                return False
            except mysql.connector.Error:
                print("  ✓ Valid: Unique constraint works (duplicate review rejected)")
                self.connection.rollback()
        
        return True
    
    def run_all_checks(self):
        """Run all verification checks."""
        print("HBnB Database Verification")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.connect():
            return False
        
        try:
            # Run checks
            tables_ok = self.check_tables()
            self.check_data_counts()
            admin_ok = self.verify_admin_user()
            amenities_ok = self.verify_initial_amenities()
            constraints_ok = self.test_foreign_key_constraints()
            
            # Show table structures
            print("\n" + "=" * 60)
            print("Table Structures:")
            for table in ['users', 'places', 'amenities', 'reviews']:
                self.check_table_structure(table)
            
            # Summary
            print("\n" + "=" * 60)
            print("VERIFICATION SUMMARY:")
            print("-" * 40)
            print(f"  Tables:         {'✓ PASS' if tables_ok else '✗ FAIL'}")
            print(f"  Admin User:     {'✓ PASS' if admin_ok else '✗ FAIL'}")
            print(f"  Amenities:      {'✓ PASS' if amenities_ok else '✗ FAIL'}")
            print(f"  Constraints:    {'✓ PASS' if constraints_ok else '✗ FAIL'}")
            
            overall = tables_ok and admin_ok and amenities_ok and constraints_ok
            print("-" * 40)
            print(f"  OVERALL:        {'✓ PASS' if overall else '✗ FAIL'}")
            
            return overall
            
        finally:
            self.disconnect()

def main():
    """Main function."""
    # Check command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Verify HBnB database setup')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--database', default='hbnb_db', help='Database name')
    parser.add_argument('--username', default='hbnb_user', help='Database username')
    parser.add_argument('--password', default='hbnb_password_123', help='Database password')
    
    args = parser.parse_args()
    
    # Run verification
    verifier = DatabaseVerifier(
        host=args.host,
        database=args.database,
        username=args.username,
        password=args.password
    )
    
    success = verifier.run_all_checks()
    
    if success:
        print("\n✅ Database setup is CORRECT!")
        sys.exit(0)
    else:
        print("\n❌ Database setup has ISSUES!")
        sys.exit(1)

if __name__ == "__main__":
    main()
