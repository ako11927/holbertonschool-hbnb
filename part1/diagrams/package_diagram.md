# Task 0: High-Level Package Diagram

## Diagram using Mermaid.js

```mermaid
graph TB
    subgraph "Presentation Layer"
        A["API Endpoints<br/>/users, /places, /reviews"]
        C["Controllers<br/>UserController, PlaceController"]
        S["Services<br/>UserService, PlaceService"]
        D["Data Transfer Objects<br/>(DTOs)"]
    end
    
    subgraph "Business Logic Layer"
        F["HBnB Facade<br/>(Facade Pattern)"]
        M["Models<br/>User, Place, Review, Amenity"]
        B["Business Rules<br/>Validation & Logic"]
    end
    
    subgraph "Persistence Layer"
        R["Repository Pattern<br/>UserRepo, PlaceRepo"]
        DB[("Database<br/>MySQL/PostgreSQL")]
        MAP["Data Mappers"]
    end
    
    A --> F
    C --> F
    S --> F
    D --> F
    
    F --> M
    F --> B
    
    B --> R
    R --> DB
    R --> MAP
    
    style A fill:#e1f5fe
    style C fill:#e1f5fe
    style S fill:#e1f5fe
    style D fill:#e1f5fe
    style F fill:#f3e5f5
    style M fill:#f3e5f5
    style B fill:#f3e5f5
    style R fill:#e8f5e8
    style DB fill:#e8f5e8
    style MAP fill:#e8f5e8
