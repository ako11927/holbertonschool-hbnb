#!/bin/bash
echo "Testing API endpoints while server is running..."

# Get all places
echo -e "\n1. GET /api/v1/places/"
curl -s http://localhost:5000/api/v1/places/ | python3 -m json.tool

# Get specific place (using first place ID from sample)
echo -e "\n\n2. GET /api/v1/places/<id>/"
# We'll need to extract a place ID first
PLACE_ID=$(curl -s http://localhost:5000/api/v1/places/ | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0]['id'] if data else '')")
if [ -n "$PLACE_ID" ]; then
    curl -s http://localhost:5000/api/v1/places/$PLACE_ID/ | python3 -m json.tool
else
    echo "No places found"
fi

# Get user ID for POST test
echo -e "\n\n3. Getting user ID for testing..."
USER_ID=$(curl -s http://localhost:5000/api/v1/places/ | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data and data[0].get('owner_id'):
        print(data[0]['owner_id'])
    else:
        # Try to get from sample data
        print('212f2e51-0933-4e4f-a9c3-d756288593f6')  # From server output
except:
    print('212f2e51-0933-4e4f-a9c3-d756288593f6')  # Default from server output
")

echo "Using user ID: $USER_ID"

# Create a new place
echo -e "\n\n4. POST /api/v1/places/"
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mountain Retreat",
    "description": "Beautiful mountain cabin with great views",
    "price": 220.0,
    "latitude": 39.7392,
    "longitude": -104.9903,
    "owner_id": "'"$USER_ID"'",
    "amenities": []
  }' | python3 -m json.tool

# Get all places again to see the new one
echo -e "\n\n5. GET /api/v1/places/ (after POST)"
curl -s http://localhost:5000/api/v1/places/ | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Total places: {len(data)}')
for i, place in enumerate(data[:3], 1):
    print(f'{i}. {place[\"title\"]} - ${place[\"price\"]}')"

# Get all reviews
echo -e "\n\n6. GET /api/v1/reviews/"
curl -s http://localhost:5000/api/v1/reviews/ | python3 -m json.tool
