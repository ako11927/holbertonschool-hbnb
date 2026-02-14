#!/bin/bash

# HBnB Database Setup Script
# This script sets up the HBnB database with schema and initial data

# Configuration
DB_NAME="hbnb_db"
DB_USER="hbnb_user"
DB_PASSWORD="hbnb_password_123"
DB_HOST="localhost"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

print_step() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Check if MySQL is installed
check_mysql() {
    if ! command -v mysql &> /dev/null; then
        print_error "MySQL is not installed. Please install MySQL and try again."
        exit 1
    fi
    print_success "MySQL is installed"
}

# Check if required SQL files exist
check_sql_files() {
    local required_files=("schema.sql" "initial_data.sql" "test_crud_operations.sql")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "sql/$file" ]; then
            print_error "Required SQL file not found: sql/$file"
            exit 1
        fi
    done
    print_success "All SQL files found"
}

# Get MySQL root password
get_root_password() {
    if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
        read -sp "Enter MySQL root password: " MYSQL_ROOT_PASSWORD
        echo
    fi
}

# Test MySQL connection
test_mysql_connection() {
    if ! mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1" &> /dev/null; then
        print_error "Cannot connect to MySQL with provided root password"
        exit 1
    fi
    print_success "MySQL connection successful"
}

# Create database and user
setup_database() {
    print_step "Creating database and user"
    
    # Create database
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "Database '$DB_NAME' created"
    else
        print_error "Failed to create database '$DB_NAME'"
        exit 1
    fi
    
    # Create user and grant privileges
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE USER IF NOT EXISTS '$DB_USER'@'$DB_HOST' IDENTIFIED BY '$DB_PASSWORD';" 2>/dev/null
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'$DB_HOST';" 2>/dev/null
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "FLUSH PRIVILEGES;" 2>/dev/null
    
    print_success "User '$DB_USER' created with privileges"
}

# Execute SQL files
execute_sql_files() {
    print_step "Executing SQL scripts"
    
    # Execute schema.sql
    print_info "Creating tables..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" < sql/schema.sql
    if [ $? -eq 0 ]; then
        print_success "Tables created successfully"
    else
        print_error "Failed to create tables"
        exit 1
    fi
    
    # Execute initial_data.sql
    print_info "Inserting initial data..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" < sql/initial_data.sql
    if [ $? -eq 0 ]; then
        print_success "Initial data inserted"
    else
        print_error "Failed to insert initial data"
        exit 1
    fi
}

# Test the database
test_database() {
    print_step "Testing database"
    
    # Test CRUD operations
    print_info "Running CRUD operations test..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" < sql/test_crud_operations.sql 2>&1 | tail -20
    
    # Quick verification
    print_info "Quick verification..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" -e "
        SELECT 'Users:' AS table_name, COUNT(*) AS count FROM users
        UNION ALL
        SELECT 'Places:', COUNT(*) FROM places
        UNION ALL
        SELECT 'Amenities:', COUNT(*) FROM amenities
        UNION ALL
        SELECT 'Reviews:', COUNT(*) FROM reviews
        UNION ALL
        SELECT 'Place_Amenities:', COUNT(*) FROM place_amenities;
    " 2>/dev/null
    
    # Verify admin user
    print_info "Verifying admin user..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" -e "
        SELECT 
            'Admin User' AS check_name,
            CASE 
                WHEN COUNT(*) = 1 AND is_admin = TRUE THEN '✓ Present and is admin'
                ELSE '✗ Missing or not admin'
            END AS status
        FROM users 
        WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
    " 2>/dev/null
    
    # Verify initial amenities
    print_info "Verifying initial amenities..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" -e "
        SELECT 
            'Initial Amenities' AS check_name,
            CASE 
                WHEN COUNT(*) = 3 THEN '✓ All present'
                ELSE CONCAT('✗ Missing: ', 3 - COUNT(*), ' of 3')
            END AS status
        FROM amenities 
        WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning');
    " 2>/dev/null
}

# Generate connection string
generate_connection_info() {
    print_step "Connection Information"
    
    echo -e "${YELLOW}Database Configuration:${NC}"
    echo "  Database Name: $DB_NAME"
    echo "  Username:      $DB_USER"
    echo "  Password:      $DB_PASSWORD"
    echo "  Host:          $DB_HOST"
    echo ""
    echo -e "${YELLOW}Connection Strings:${NC}"
    echo "  MySQL CLI:     mysql -u $DB_USER -p'$DB_PASSWORD' -h $DB_HOST $DB_NAME"
    echo "  Python SQLAlchemy: mysql+pymysql://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME"
    echo "  Flask Config:  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME'"
    echo ""
    echo -e "${YELLOW}Test Commands:${NC}"
    echo "  Test connection: mysql -u $DB_USER -p'$DB_PASSWORD' -h $DB_HOST -e 'SELECT \"Connected successfully\"'"
    echo "  List tables:     mysql -u $DB_USER -p'$DB_PASSWORD' -h $DB_HOST $DB_NAME -e 'SHOW TABLES;'"
}

# Main execution
main() {
    echo -e "${YELLOW}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║           HBnB Database Setup Script             ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Check prerequisites
    check_mysql
    check_sql_files
    
    # Get MySQL root password
    get_root_password
    
    # Test connection
    test_mysql_connection
    
    # Setup database
    setup_database
    
    # Execute SQL files
    execute_sql_files
    
    # Test database
    test_database
    
    # Show connection information
    generate_connection_info
    
    echo -e "\n${GREEN}Database setup completed successfully!${NC}"
    echo "You can now run the HBnB application with the database configuration above."
}

# Run main function
main "$@"
