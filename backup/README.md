# HBnB Clone - Part 2

><<><><><$$ Part 2 $$><><><>><><<>#$#
><<><><>Project Overview<><><<>><

This is the second part of the HBnB (Holberton BnB) clone project, implementing a RESTful API for a vacation rental platform similar to Airbnb. The application is built using Flask and follows a clean architecture with clear separation between Presentation, Business Logic, and Persistence layers.

><><<><><Architecture><><><<><><>

The project follows a **modular architecture** with three main layers:

presentation/ # API layer (Flask-RESTx)
business_logic/ # Core business logic and models
persistence/ # Data storage (in-memory for now)


**Key Design Patterns:**
- **Facade Pattern**: Simplified interface to complex business logic
- **Repository Pattern**: Abstract data access layer  
- **MVC-like Structure**: Clear separation of concerns

><<>><><<<></\/\+=-Quick Start-=+/\/\><><<><><<

### Prerequisites
- Python 3.8+
- pip (Python package manager)

<<<>><><>/\/\<Installation>/\/\<><><<<<>>>

1. **Clone and navigate to the project:**
    bash
    cd holbertonschool-hbnb/part2
2. **Create and activate virtual environment:**
    bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies:**
    pip install -r requirements.txt
4. **Run the application:**
    python run.py
5. **Access the API:**
    API Base URL: http://localhost:5000/api/v1

Swagger Documentation: http://localhost:5000/api/v1/docs/

API Status: http://localhost:5000/api/v1/status

<><><API Documentation><><><

For comprehensive API documentation including all endpoints, request/response formats, and examples, see:

API_DOCUMENTATION.md

<><><//\ Testing //><><><

Run All Tests
bash
./run_tests.sh
Run Specific Tests
bash
# Run unit tests
python -m unittest discover tests -v

# Run individual test file
python -m unittest tests.test_api
Manual Testing with cURL
See the testing examples in API_DOCUMENTATION.md or use the included run_tests.sh script.

<=-=-> Project Structure <-=-=><

text
holbertonschool-hbnb/part2/
├── API_DOCUMENTATION.md     # Complete API documentation
├── README.md                # This file
├── run_tests.sh             # Test automation script
├── app.py                   # Application factory
├── run.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── presentation/            # API layer
│   ├── api/
│   │   └── v1/
│   │       ├── user_routes.py      # User endpoints
│   │       ├── amenity_routes.py   # Amenity endpoints
│   │       ├── place_routes.py     # Place endpoints
│   │       ├── review_routes.py    # Review endpoints
│   │       ├── routes.py           # Main API routes
│   │       └── errors.py           # Error handlers
├── business_logic/          # Core business logic
│   ├── facade.py            # Facade pattern implementation
│   ├── exceptions.py        # Custom exceptions
│   ├── models/              # Business models
│   │   ├── base_model.py    # Base model class
│   │   ├── user.py          # User model
│   │   ├── place.py         # Place model
│   │   ├── review.py        # Review model
│   │   ├── amenity.py       # Amenity model
│   │   ├── city.py          # City model
│   │   └── state.py         # State model
│   └── services/            # Business services
├── persistence/             # Data layer
│   ├── base_repository.py   # Repository interface
│   └── in_memory_repository.py  # In-memory implementation
├── utils/                   # Utilities
│   └── validators.py        # Validation functions
└── tests/                   # Test suite
    ├── test_api.py          # API tests
    ├── __init__.py
    └── __main__.py
<><><>>>,,,<<\//\// Features Implemented \//\//\>>,,,>>><><><

<<><><><///| Core Business Models |///><><><>><>

User: Platform users with email/password authentication

Place: Rental properties with coordinates, pricing, and amenities

Review: User reviews with ratings (1-5 stars)

Amenity: Property features (WiFi, Pool, etc.)

City & State: Geographical hierarchy

<><><<'"'"'"API Endpoints"'"'"'><><><

Users: GET, POST, PUT operations

Amenities: GET, POST, PUT operations

Places: GET, POST, PUT operations with relationship handling

Reviews: GET, POST, PUT, DELETE operations (only entity with DELETE)

<><><Validation & Error Handling><><><

Email format validation

Password strength validation

Coordinate range validation (-90 to 90 latitude, -180 to 180 longitude)

Rating validation (1-5)

Price validation (non-negative)

Comprehensive error responses

<><><:":",././\ Testing/..,":":><><><

Unit tests for all API endpoints

Integration tests with cURL

Automated test script

Edge case testing

<><><[][]\||Documentation||//[][]><><><

Interactive Swagger UI

Comprehensive API documentation

Clear usage examples

Error code documentation

<<>><><><</||Configuration||/>><><><<><

The application supports multiple environments:

Environment	Configuration File	Use Case
Development	config.py (DevelopmentConfig)	Local development
Testing	config.py (TestingConfig)	Running tests
Production	config.py (ProductionConfig)	Production deployment
Set environment variable to change config:

bash
export FLASK_CONFIG=testing  # For testing environment
<""':(())>>><<Key Implementation Details>>><<<(()):'""><

Security Features
Passwords are never exposed in API responses

Email format validation

Input sanitization on all endpoints

Relationship Handling
Places show owner details and amenities

Reviews show user information

Cities belong to states

Reviews are linked to both users and places

Data Integrity
UUIDs for all entities

Timestamps (created_at, updated_at)

Referential integrity checks

Duplicate prevention

<<>><><><Important Notes>><<>><><>

Persistence: Currently uses in-memory storage. Data is lost on server restart.

Authentication: Basic implementation. JWT/OAuth would be added in production.

DELETE Operations: Only reviews support DELETE in this implementation.

File Uploads: Not implemented in this phase.

Pagination: All list endpoints return all results (no pagination).

<<>><><><Future Improvement><<>><><>><<>>

Database Integration: Replace in-memory with SQLAlchemy + PostgreSQL

Authentication: JWT tokens or OAuth2

File Uploads: Image upload for places and user profiles

Pagination: Limit/offset for list endpoints

Search & Filtering: Advanced search for places

Booking System: Reservation management

Payment Integration: Stripe/PayPal integration

<<>><><>< Troubleshooting >><<>><><>

Common Issues:
Port already in use:

bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
Module import errors:

bash
# Make sure you're in the right directory
pwd  # Should show /path/to/holbertonschool-hbnb/part2

# Install dependencies
pip install -r requirements.txt
Permission denied on run_tests.sh:

bash
chmod +x run_tests.sh
<<>><<><>< License>><<>><<><><

This project is part of the Holberton School curriculum.

<<>><<><><Acknowledgments>><<>><<><><

Holberton School mentors and peers

Flask and Flask-RESTx communities

REST API design best practices community

<^>^<^>^<^>^<^>^<^>^<^>^<^>^
👥 CONTRIBUTORS
<^>^<^>^<^>^<^>^<^>^<^>^<^>^

✦ Ahmed Khaled - Full-stack implementation
• GitHub: ako11927

✦ Rinad Fahad - API endpoints & business logic
• GitHub: Rinadf

✦ Shadan Khaled - Testing & documentation
• GitHub: ShadanKhaled


