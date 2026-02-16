#!/bin/bash
echo "=== Testing Amenity Endpoints with cURL ==="

# Start the app in background
echo "Starting Flask app..."
python3 run.py &
APP_PID=$!
sleep 3

echo -e "\n1. Creating first amenity..."
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n2. Creating second amenity..."
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n3. Getting all amenities..."
curl -X GET http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n"

echo -e "\n4. Getting first amenity (need to copy ID from above)..."
echo "Replace AMENITY_ID with actual amenity ID from step 1"

echo -e "\n5. Documentation available at: http://localhost:5000/api/v1/"

# Stop the app
kill $APP_PID 2>/dev/null
echo -e "\nApplication stopped"
