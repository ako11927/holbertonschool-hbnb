# HBnB API Documentation

## Base URL

http://localhost:5000/api/v1


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
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]

POST /users/
Create a new user.

Parameters:

email (required): Valid email address

password (required): At least 6 characters, containing letters and numbers

first_name (optional): First name

last_name (optional): Last name

GET /users/{user_id}
Retrieve a specific user.

PUT /users/{user_id}
Update user information.

Places
GET /places/
Retrieve all places.

POST /places/
Create a new place.

Parameters:

user_id (required): ID of the owner user

name (required): Place name

description (optional): Description

number_rooms (required): Non-negative integer

number_bathrooms (required): Non-negative integer

max_guest (required): Non-negative integer

price_by_night (required): Non-negative number

latitude (required): Between -90 and 90

longitude (required): Between -180 and 180

city_id (required): ID of the city

amenity_ids (optional): List of amenity IDs

GET /places/{place_id}
Retrieve a specific place with owner and amenities.

PUT /places/{place_id}
Update place information.

Reviews
GET /reviews/
Retrieve all reviews.

POST /reviews/
Create a new review.

Parameters:

user_id (required): ID of the reviewer

place_id (required): ID of the place being reviewed

text (required): Review text

rating (required): Integer between 1 and 5

GET /reviews/{review_id}
Retrieve a specific review with user details.

PUT /reviews/{review_id}
Update review information.

DELETE /reviews/{review_id}
Delete a review.

Amenities
GET /amenities/
Retrieve all amenities.

POST /amenities/
Create a new amenity.

Parameters:

name (required): Amenity name

description (optional): Description

icon (optional): Icon name

category (optional): One of: basic, safety, luxury, accessibility, kitchen, bathroom

GET /amenities/{amenity_id}
Retrieve a specific amenity.

PUT /amenities/{amenity_id}
Update amenity information.

Testing
Running Tests
bash
# Run unit tests
python -m unittest discover tests -v

# Run cURL tests
./run_tests.sh
Example cURL Commands
Create a user:

bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -d "email=test@example.com&password=test123&first_name=John&last_name=Doe"
Create a place:

bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -d "user_id=user-uuid&name=Beautiful Apartment&number_rooms=2&number_bathrooms=1&max_guest=4&price_by_night=100&latitude=40.7128&longitude=-74.0060&city_id=city-uuid"
Error Codes
200: Success

201: Created

204: No Content (for DELETE)

400: Bad Request (validation failed)

404: Not Found

409: Conflict (duplicate entry)

500: Internal Server Error

text

## Summary

I've implemented a complete API with:

### ✅ User Endpoints:
- GET `/users/` - List all users
- POST `/users/` - Create user
- GET `/users/{id}` - Get specific user
- PUT `/users/{id}` - Update user

### ✅ Amenity Endpoints:
- GET `/amenities/` - List all amenities
- POST `/amenities/` - Create amenity
- GET `/amenities/{id}` - Get specific amenity
- PUT `/amenities/{id}` - Update amenity

### ✅ Place Endpoints:
- GET `/places/` - List all places
- POST `/places/` - Create place (with validation)
- GET `/places/{id}` - Get place with relationships
- PUT `/places/{id}` - Update place

### ✅ Review Endpoints:
- GET `/reviews/` - List all reviews
- POST `/reviews/` - Create review
- GET `/reviews/{id}` - Get review with user
- PUT `/reviews/{id}` - Update review
- DELETE `/reviews/{id}` - Delete review (only entity with delete)

### ✅ Testing & Validation:
- Unit tests with unittest
- Enhanced validation utilities
- cURL testing script
- Comprehensive error handling
- Swagger documentation via Flask-RESTx

### Key Features:
1. **Proper Validation**: Email, password, coordinates, ratings, prices
2. **Relationship Handling**: Places show owners and amenities, reviews show users
3. **Security**: Passwords never exposed in responses
4. **Error Handling**: Clear error messages with appropriate HTTP codes
5. **Testing**: Both unit tests and integration tests
6. **Documentation**: Comprehensive API documentation

The implementation follows RESTful principles and is ready for black-box testing. All endpoints return proper status codes and validate input data according to the business rules.
