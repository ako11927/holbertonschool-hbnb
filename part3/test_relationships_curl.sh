#!/bin/bash

echo "Testing HBnB API Relationships..."
echo "=================================="

BASE_URL="http://127.0.0.1:5000/api/v1"

# 1. Create a user (owner)
echo -e "\n1. Creating owner user..."
OWNER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "PropertyOwner",
    "email": "john.owner@example.com",
    "password": "ownerpass123"
  }')

echo "Response: $OWNER_RESPONSE"
OWNER_ID=$(echo $OWNER_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Owner ID: $OWNER_ID"

# 2. Create another user (reviewer)
echo -e "\n2. Creating reviewer user..."
REVIEWER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Traveler",
    "email": "jane.reviewer@example.com",
    "password": "reviewerpass123"
  }')

echo "Response: $REVIEWER_RESPONSE"
REVIEWER_ID=$(echo $REVIEWER_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Reviewer ID: $REVIEWER_ID"

# 3. Create amenities
echo -e "\n3. Creating amenities..."
AMENITY_IDS=()
for AMENITY in "WiFi" "Swimming Pool" "Parking"; do
  AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$AMENITY\"}")
  
  AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
  AMENITY_IDS+=("$AMENITY_ID")
  echo "Created amenity '$AMENITY' with ID: $AMENITY_ID"
done

# 4. Create a place with owner relationship
echo -e "\n4. Creating place with owner relationship..."
PLACE_DATA=$(cat <<EOF
{
  "title": "Beautiful Villa",
  "description": "A stunning villa with amazing amenities",
  "price": 250.00,
  "address": "123 Luxury Lane",
  "city": "Beverly Hills",
  "max_guests": 6,
  "bedrooms": 3,
  "bathrooms": 2,
  "owner_id": "$OWNER_ID",
  "amenities": ["${AMENITY_IDS[0]}", "${AMENITY_IDS[1]}"]
}
EOF
)

PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places" \
  -H "Content-Type: application/json" \
  -d "$PLACE_DATA")

echo "Response: $PLACE_RESPONSE"
PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Place ID: $PLACE_ID"

# 5. Get the place with relationships
echo -e "\n5. Getting place with relationships..."
curl -s -X GET "$BASE_URL/places/$PLACE_ID" | python -m json.tool

# 6. Create a review with relationships
echo -e "\n6. Creating review with relationships..."
REVIEW_DATA=$(cat <<EOF
{
  "text": "Amazing place! The amenities were fantastic and the location was perfect.",
  "rating": 5,
  "user_id": "$REVIEWER_ID",
  "place_id": "$PLACE_ID"
}
EOF
)

REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews" \
  -H "Content-Type: application/json" \
  -d "$REVIEW_DATA")

echo "Response: $REVIEW_RESPONSE"
REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Review ID: $REVIEW_ID"

# 7. Get user places (One-to-Many relationship)
echo -e "\n7. Testing User -> Places relationship..."
echo "Getting places owned by user $OWNER_ID:"
# Note: This endpoint needs to be implemented in the controller
# For now, we'll get the place and check its owner

# 8. Get place reviews (One-to-Many relationship)
echo -e "\n8. Testing Place -> Reviews relationship..."
echo "Getting reviews for place $PLACE_ID:"
curl -s -X GET "$BASE_URL/reviews?place_id=$PLACE_ID" | python -m json.tool 2>/dev/null || echo "Endpoint not implemented yet"

# 9. Test adding amenity to place (Many-to-Many relationship)
echo -e "\n9. Testing Place <-> Amenity relationship..."
echo "Adding 'Parking' amenity to place..."
# Note: This would require a dedicated endpoint

# 10. Clean up (optional)
echo -e "\n10. Test data created successfully!"
echo "To clean up, manually delete:"
echo "  - Review: $REVIEW_ID"
echo "  - Place: $PLACE_ID"
echo "  - Amenities: ${AMENITY_IDS[@]}"
echo "  - Users: $OWNER_ID, $REVIEWER_ID"

echo -e "\nRelationship testing complete!"
