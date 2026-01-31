# HBnB Database Entity Relationship Diagrams

## Complete Database Schema

```mermaid
erDiagram
    USERS {
        string id PK "CHAR(36)"
        string first_name "VARCHAR(255)"
        string last_name "VARCHAR(255)"
        string email UK "VARCHAR(255)"
        string password "VARCHAR(255)"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at
        datetime updated_at
    }
    
    PLACES {
        string id PK "CHAR(36)"
        string title "VARCHAR(255)"
        text description
        decimal price "DECIMAL(10,2)"
        float latitude
        float longitude
        string address "VARCHAR(500)"
        string city "VARCHAR(100)"
        integer max_guests
        integer bedrooms
        integer bathrooms
        string owner_id FK
        datetime created_at
        datetime updated_at
    }
    
    REVIEWS {
        string id PK "CHAR(36)"
        text text
        integer rating "1-5"
        string user_id FK
        string place_id FK
        datetime created_at
        datetime updated_at
    }
    
    AMENITIES {
        string id PK "CHAR(36)"
        string name "VARCHAR(255)"
        datetime created_at
        datetime updated_at
    }
    
    PLACE_AMENITIES {
        string place_id FK,PK
        string amenity_id FK,PK
    }
    
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES }|--|| PLACE_AMENITIES : "links_to"
    AMENITIES }|--|| PLACE_AMENITIES : "links_to"
