#!/usr/bin/env python3
"""Generate bcrypt password hashes for SQL scripts."""

import bcrypt
import sys

def generate_hash(password, rounds=12):
    """Generate bcrypt hash for a password."""
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def main():
    """Main function to generate password hashes."""
    print("HBnB Password Hash Generator")
    print("=" * 40)
    
    # Default passwords to hash
    passwords = {
        'admin1234': 'Admin user password',
        'Password123!': 'Regular user password'
    }
    
    print("\nGenerating bcrypt hashes (12 rounds):")
    print("-" * 40)
    
    for password, description in passwords.items():
        hashed = generate_hash(password)
        print(f"\n{description}:")
        print(f"  Password: {password}")
        print(f"  Hash:     {hashed}")
    
    # Generate hash for custom password
    print("\n" + "=" * 40)
    print("Custom Password Hash Generation")
    print("-" * 40)
    
    while True:
        try:
            custom_password = input("\nEnter password to hash (or 'quit' to exit): ").strip()
            
            if custom_password.lower() == 'quit':
                break
            
            if not custom_password:
                print("Password cannot be empty!")
                continue
            
            hashed = generate_hash(custom_password)
            print(f"\nPassword: {custom_password}")
            print(f"Hash:     {hashed}")
            
            # Generate SQL INSERT statement
            print("\nSQL INSERT statement:")
            print(f"INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (")
            print(f"    UUID(),")
            print(f"    'First',")
            print(f"    'Last',")
            print(f"    'email@example.com',")
            print(f"    '{hashed}',")
            print(f"    FALSE")
            print(f");")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Install bcrypt if not available
    try:
        import bcrypt
    except ImportError:
        print("bcrypt module not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bcrypt"])
        import bcrypt
    
    main()
