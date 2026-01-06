#!/bin/bash

# Run API tests
echo "Running API tests..."
python -m unittest discover tests -v

# Run cURL tests
echo -e "\nRunning cURL tests..."

# Test API status
echo -e "\n1. Testing API status:"
curl -X GET http://localhost:5000/api/v1/status

# Test user creation
echo -e "\n\n2. Testing user creation:"
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=test123&first_name=Test&last_name=User"

# Test getting all users
echo -e "\n\n3. Testing get all users:"
curl -X GET http://localhost:5000/api/v1/users/

# Test amenity creation
echo -e "\n\n4. Testing amenity creation:"
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=WiFi&description=High-speed internet&category=basic"

echo -e "\n\nAll tests completed!"
