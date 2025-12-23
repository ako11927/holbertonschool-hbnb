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

