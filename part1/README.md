# HBnB Evolution – Part 1
## Technical Documentation

---

## Introduction

This document provides the technical documentation for **Part 1** of the HBnB Evolution project.  
The goal of this phase is to define the **architecture and design** of the application before implementation.

HBnB Evolution is a simplified AirBnB-like application that allows:
- User management
- Place listings
- Reviews
- Amenities management

This documentation serves as a blueprint for future development phases.

---

## Task 0: High-Level Package Diagram

### Objective

The objective of this task is to illustrate the **high-level architecture** of the HBnB Evolution application using a **three-layered architecture** and the **Facade design pattern**.

This diagram provides a conceptual overview of how the application is structured and how the different layers communicate with each other.

---

## Architecture Overview

The HBnB Evolution application follows a **layered architecture** composed of three main layers:

1. Presentation Layer (Services / API)
2. Business Logic Layer (Core & Models)
3. Persistence Layer (Data Access)

Each layer has a clearly defined responsibility, ensuring separation of concerns, maintainability, and scalability.

---

## Layer Responsibilities

### 1. Presentation Layer (Services / API)

**Responsibilities:**
- Handle user interactions through API endpoints
- Validate input data
- Send requests to the Business Logic layer
- Return responses to the client

**Characteristics:**
- Does not contain business rules
- Does not interact directly with the database

**Examples:**
- UserService
- PlaceService
- ReviewService
- AmenityService

---

### 2. Business Logic Layer (Core & Models)

**Responsibilities:**
- Contain all business rules
- Manage core entities and their relationships
- Coordinate operations between services and persistence
- Enforce validation and constraints

**Key Components:**
- Facade (HBnBFacade)
- User
- Place
- Review
- Amenity

This layer acts as the central point of the application logic.

---

### 3. Persistence Layer (Data Access)

**Responsibilities:**
- Store and retrieve data
- Abstract database operations
- Provide repositories for entities

**Characteristics:**
- No business logic
- Interacts directly with the database (implemented in Part 3)

**Examples:**
- UserRepository
- PlaceRepository
- ReviewRepository
- AmenityRepository

---

## Facade Design Pattern

The **Facade Pattern** is used to simplify communication between the Presentation Layer and the Business Logic Layer.

### Benefits:
- Provides a single entry point to the business logic
- Reduces coupling between layers
- Improves readability and maintainability
- Makes testing easier

The Presentation Layer interacts **only** with the Facade and never directly with models or repositories.

---

## High-Level Package Diagram (UML)

The following UML package diagram illustrates the three-layer architecture and the communication between layers using the Facade pattern.

```mermaid
classDiagram

package "Presentation Layer\n(Services / API)" {
    class UserService
    class PlaceService
    class ReviewService
    class AmenityService
}

package "Business Logic Layer\n(Core & Models)" {
    class HBnBFacade <<Facade>>
    class User
    class Place
    class Review
    class Amenity
}

package "Persistence Layer\n(Data Access)" {
    class UserRepository
    class PlaceRepository
    class ReviewRepository
    class AmenityRepository
}

UserService --> HBnBFacade
PlaceService --> HBnBFacade
ReviewService --> HBnBFacade
AmenityService --> HBnBFacade

HBnBFacade --> UserRepository
HBnBFacade --> PlaceRepository
HBnBFacade --> ReviewRepository
HBnBFacade --> AmenityRepository

---

## Task 1: Detailed Class Diagram (Business Logic Layer)

### Objective

The objective of this task is to design a **detailed UML class diagram** for the **Business Logic layer** of the HBnB Evolution application.

This diagram defines the core entities, their attributes, methods, and relationships, and serves as a blueprint for the implementation phase.

---

## Business Logic Layer Overview

The Business Logic layer contains the core models of the application and enforces all business rules.  
Each entity is uniquely identified by an `id` and includes audit fields for creation and update timestamps.

The main entities are:
- User
- Place
- Review
- Amenity

---

## Entity Descriptions

### User
Represents a registered user of the application.

**Attributes:**
- id
- first_name
- last_name
- email
- password
- is_admin
- created_at
- updated_at

**Responsibilities:**
- Own places
- Write reviews

---

### Place
Represents a property listed by a user.

**Attributes:**
- id
- title
- description
- price
- latitude
- longitude
- created_at
- updated_at

**Responsibilities:**
- Belongs to a user (owner)
- Can have multiple amenities
- Can receive reviews

---

### Review
Represents a review written by a user for a place.

**Attributes:**
- id
- rating
- comment
- created_at
- updated_at

**Responsibilities:**
- Linked to one user
- Linked to one place

---

### Amenity
Represents an amenity that can be associated with places.

**Attributes:**
- id
- name
- description
- created_at
- updated_at

**Responsibilities:**
- Can be linked to multiple places

---

## UML Class Diagram

The following UML class diagram illustrates the entities, their attributes, and their relationships.

```mermaid
classDiagram

class User {
    +id
    +first_name
    +last_name
    +email
    +password
    +is_admin
    +created_at
    +updated_at
}

class Place {
    +id
    +title
    +description
    +price
    +latitude
    +longitude
    +created_at
    +updated_at
}

class Review {
    +id
    +rating
    +comment
    +created_at
    +updated_at
}

class Amenity {
    +id
    +name
    +description
    +created_at
    +updated_at
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has
