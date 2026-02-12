# HBnB Evolution - Technical Documentation
## Part 1: Architecture and Design Documentation

**Date:** December 2025  
**Version:** 1.0  
**Author:** [Ahmed Khaled Alomani, Alsmail Saud Alanoud, Amaal Ghazi Alotaibi]

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Business Logic Layer Design](#business-logic-layer-design)
4. [Sequence Flows](#sequence-flows)
5. [Database Design Considerations](#database-design-considerations)
6. [API Specifications](#api-specifications)
7. [Design Patterns Used](#design-patterns-used)
8. [Business Rules Summary](#business-rules-summary)
  
---

## Executive Summary

HBnB Evolution is an AirBnB-like application designed with a three-layer architecture. This document provides comprehensive technical documentation including architecture diagrams, class designs, and sequence flows for the core operations.

### Key Features
- User registration and profile management
- Property listing and management
- Review and rating system
- Amenity management
- Search and filtering capabilities

### Technology Stack
- **Architecture**: Three-layer (Presentation, Business Logic, Persistence)
- **Pattern**: Facade Pattern for layer communication
- **Database**: SQL-based (MySQL/PostgreSQL)
- **API**: RESTful design

---

## Architecture Overview

### High-Level Package Diagram
![Package Diagram](../diagrams/package_diagram.md)

The application follows a three-layer architecture:

1. **Presentation Layer**: Handles user interactions via REST API
2. **Business Logic Layer**: Contains core business rules and entities
3. **Persistence Layer**: Manages data storage and retrieval

### Facade Pattern Implementation
The **HBnB Facade** acts as a unified interface between layers, hiding complexity and reducing coupling.

---

## Business Logic Layer Design

### Detailed Class Diagram
![Class Diagram](../diagrams/class_diagram.md)

### Entity Descriptions

#### 1. User Entity
- **Purpose**: Manages user accounts and authentication
- **Attributes**: firstName, lastName, email, password, isAdmin
- **Relationships**: Owns Places, Writes Reviews

#### 2. Place Entity
- **Purpose**: Represents property listings
- **Attributes**: title, description, price, latitude, longitude
- **Relationships**: Owned by User, Has Reviews, Contains Amenities

#### 3. Review Entity
- **Purpose**: Manages user reviews and ratings
- **Attributes**: rating (1-5), comment
- **Relationships**: Written by User, Belongs to Place

#### 4. Amenity Entity
- **Purpose**: Defines property amenities/features
- **Attributes**: name, description
- **Relationships**: Associated with Places (Many-to-Many)

### Inheritance Hierarchy
All entities inherit from `BaseModel` which provides:
- Automatic ID generation (UUID)
- Creation and update timestamps
- Common CRUD operations

---

## Sequence Flows

### Key Operations Documented
Complete sequence diagrams available in [sequence_diagrams.md](../diagrams/sequence_diagrams.md)

#### 1. User Registration Flow
- Client → API → Controller → Service → Facade → Repository → Database
- Includes validation, password encryption, and response formatting

#### 2. Place Creation Flow
- Requires authenticated user
- Includes coordinate validation, price validation
- Establishes owner relationship

#### 3. Review Submission Flow
- Requires user to have visited the place
- Includes rating validation (1-5)
- Updates place's average rating

#### 4. Place Search Flow
- Supports filtering by price, amenities, location
- Includes pagination
- Complex database queries with JOIN operations

### Layer Interaction Patterns
All operations follow consistent patterns:
- **Request Flow**: Top-down (Presentation → Business → Persistence)
- **Response Flow**: Bottom-up (Persistence → Business → Presentation)
- **Error Handling**: Propagated with appropriate HTTP codes

---

## Database Design Considerations

### Entity Relationships
Users (1) -- (Many) Places
Users (1) -- (Many) Reviews
Places (1) -- (Many) Reviews
Places (Many) -- (Many) Amenities (via Junction Table)

### Audit Fields
All tables include:
- `id` (UUID primary key)
- `created_at` (timestamp)
- `updated_at` (timestamp)

### Indexing Strategy
Recommended indexes:
- Users: email (unique), is_admin
- Places: owner_id, price, created_at
- Reviews: user_id, place_id, created_at
- Amenities: name (unique)

---

## API Specifications

### Base URL
https://api.hbnb.example.com/v1


### Endpoints Summary

#### User Management
- `POST /users` - Register new user
- `GET /users/{id}` - Get user profile
- `PUT /users/{id}` - Update user profile
- `DELETE /users/{id}` - Delete user (admin only)

#### Place Management
- `POST /places` - Create new place (authenticated)
- `GET /places` - List places (with filters)
- `GET /places/{id}` - Get place details
- `PUT /places/{id}` - Update place (owner only)
- `DELETE /places/{id}` - Delete place (owner/admin)

#### Review Management
- `POST /places/{placeId}/reviews` - Add review (authenticated)
- `GET /places/{placeId}/reviews` - List reviews for place
- `PUT /reviews/{id}` - Update review (author only)
- `DELETE /reviews/{id}` - Delete review (author/admin)

#### Amenity Management
- `GET /amenities` - List all amenities
- `POST /amenities` - Create amenity (admin only)
- `PUT /amenities/{id}` - Update amenity (admin only)

### Authentication
- JWT-based authentication for protected endpoints
- Token in Authorization header: `Bearer {token}`

### Pagination
All list endpoints support:
- `page` (default: 1)
- `limit` (default: 20, max: 100)
- Response includes pagination metadata

---

## Design Patterns Used

### 1. Facade Pattern
- **Implementation**: HBnB Facade class
- **Purpose**: Simplify interactions between layers
- **Benefits**: Reduced coupling, centralized control

### 2. Repository Pattern
- **Implementation**: Repository classes for each entity
- **Purpose**: Abstract database operations
- **Benefits**: Easy testing, database independence

### 3. Data Transfer Object (DTO)
- **Implementation**: DTO classes for API communication
- **Purpose**: Clean data transfer between layers
- **Benefits**: Separation of concerns, validation

### 4. Template Method Pattern
- **Implementation**: BaseModel abstract class
- **Purpose**: Define common operations skeleton
- **Benefits**: Code reuse, consistent behavior

---

## Business Rules Summary

### User Rules
1. Email addresses must be unique
2. Passwords must be encrypted before storage
3. Regular users cannot modify other users' data
4. Admin flag defaults to false

### Place Rules
1. Price must be positive number
2. Coordinates must be valid (latitude: -90 to 90, longitude: -180 to 180)
3. Only owners can modify their places
4. Places require at least a title and price

### Review Rules
1. Rating must be between 1 and 5 (inclusive)
2. Users can only review places they have visited
3. One review per user per place
4. Reviews cannot be modified after 7 days

### Amenity Rules
1. Amenity names must be unique
2. Standard amenities are pre-loaded
3. Only admins can create/update amenities

### General Rules
1. All entities have audit fields (id, created_at, updated_at)
2. Soft delete for user data retention
3. Input validation at API boundary
4. Error responses follow consistent format

---

## Appendix

### A. Assumptions
1. Single currency (USD) for pricing
2. English language for content
3. Metric system for distances
4. 24-hour time format

### B. Constraints
1. Maximum image upload size: 5MB per image
2. Maximum review length: 1000 characters
3. Maximum amenities per place: 20
4. Maximum price: $10,000 per night

### C. Future Considerations
1. Multi-language support
2. Multi-currency support
3. Real-time notifications
4. Mobile app development
5. Integration with payment gateways

### D. Glossary
- **DTO**: Data Transfer Object
- **CRUD**: Create, Read, Update, Delete
- **JWT**: JSON Web Token
- **UUID**: Universally Unique Identifier
- **API**: Application Programming Interface

---

**Document Status**: Complete for Part 1 Implementation  
**Next Phase**: Part 2 - Implementation of Business Logic Layer
