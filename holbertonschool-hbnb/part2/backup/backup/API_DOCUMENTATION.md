# HBnB API Documentation

## Base URL
http://localhost:5000/api/v1

text

## Authentication
Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints

### Users

#### GET /users/
Retrieve all users.

**Response:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "email": "11927@holbertonstudents.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
POST /users/
Create a new user.

Request Body:

json
{
  "email": "11927@holbertonstudents.com",
  "password": "123456",
  "first_name": "John",
  "last_name": "Doe"
}
Parameters:

email (required): Valid email address format

password (required): Minimum 6 characters

first_name (required): First name

last_name (required): Last name

GET /users/{user_id}
Retrieve a specific user.

Example:

GET /users/a1b2c3d4-e5f6-7890-abcd-ef1234567890
PUT /users/{user_id}
Update user information.

Request Body:

json
{
  "first_name": "Jonathan",
  "last_name": "Smith"
}
Places
GET /places/
Retrieve all places.

POST /places/
Create a new place.

Request Body:

json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Modern Apartment in Riyadh",
  "description": "Beautiful 2-bedroom apartment in the heart of Riyadh with amazing city views.",
  "number_rooms": 2,
  "number_bathrooms": 2,
  "max_guest": 4,
  "price_by_night": 350.00,
  "latitude": 24.7136,
  "longitude": 46.6753,
  "city_id": "riyadh-sa-001",
  "amenity_ids": ["wifi-001", "parking-002", "pool-003"]
}
Parameters:

user_id (required): Valid user ID (must exist)

name (required): Place name

description (optional): Description

number_rooms (required): Integer >= 0

number_bathrooms (required): Integer >= 0

max_guest (required): Integer >= 0

price_by_night (required): Decimal number >= 0

latitude (required): Float between -90.0 and 90.0

longitude (required): Float between -180.0 and 180.0

city_id (required): Valid city ID

amenity_ids (optional): List of valid amenity IDs

GET /places/{place_id}
Retrieve a specific place with owner and amenities.

Example:

text
GET /places/b2c3d4e5-f6a7-8901-bcde-f23456789012
PUT /places/{place_id}
Update place information.

Request Body:

json
{
  "name": "Luxury Apartment in Riyadh Center",
  "price_by_night": 400.00,
  "description": "Updated description with new amenities"
}
Reviews
GET /reviews/
Retrieve all reviews.

POST /reviews/
Create a new review.

Request Body:

json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "place_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "text": "Excellent apartment! Clean, spacious, and great location. The host was very responsive.",
  "rating": 5
}
Parameters:

user_id (required): ID of the reviewer

place_id (required): ID of the place being reviewed

text (required): Review text

rating (required): Integer between 1 and 5

GET /reviews/{review_id}
Retrieve a specific review with user details.

Example:

text
GET /reviews/c3d4e5f6-a7b8-9012-cdef-345678901234
PUT /reviews/{review_id}
Update review information.

Request Body:

json
{
  "text": "Updated review: Still excellent but noticed some minor issues.",
  "rating": 4
}
DELETE /reviews/{review_id}
Delete a review.

Example:

DELETE /reviews/c3d4e5f6-a7b8-9012-cdef-345678901234
Amenities
GET /amenities/
Retrieve all amenities.

POST /amenities/
Create a new amenity.

Request Body:

json
{
  "name": "High-Speed WiFi",
  "description": "Fiber optic internet connection",
  "icon": "wifi",
  "category": "basic"
}
Parameters:

name (required): Amenity name

description (optional): Description

icon (optional): Icon name

category (optional): One of: basic, safety, luxury, accessibility, kitchen, bathroom

GET /amenities/{amenity_id}
Retrieve a specific amenity.

Example:

GET /amenities/wifi-001
PUT /amenities/{amenity_id}
Update amenity information.

Request Body:

json
{
  "name": "Premium WiFi",
  "description": "Ultra-fast fiber internet with multiple access points"
}
Testing
Running Tests

# Run unit tests
python -m unittest discover tests -v

# Run cURL tests
./run_tests.sh
Example cURL Commands
Create a user:

curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "11927@holbertonstudents.com",
    "password": "123456",
    "first_name": "John",
    "last_name": "Doe"
  }'
Create a place:

curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Modern Apartment in Riyadh",
    "description": "Beautiful apartment with amazing views",
    "number_rooms": 2,
    "number_bathrooms": 2,
    "max_guest": 4,
    "price_by_night": 350.00,
    "latitude": 24.7136,
    "longitude": 46.6753,
    "city_id": "riyadh-sa-001"
  }'
Create a review:

curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "place_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "text": "Great place to stay!",
    "rating": 5
  }'

Error Codes

200: Success
201: Created
204: No Content (for DELETE)
400: Bad Request (validation failed)
404: Not Found
409: Conflict (duplicate entry)
500: Internal Server Error

<^>^<^>^<^>^<^>^<^>^<^>^<^>^
CONTRIBUTORS
<^>^<^>^<^>^<^>^<^>^<^>^<^>^

✦ Ahmed Khaled - Full-stack implementation
• GitHub: ako11927

✦ Rinad Fahad - API endpoints & business logic
• GitHub: Rinadf

✦ Shadan Khaled - Testing & documentation
• GitHub: ShadanKhaled

