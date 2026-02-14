# Task 1: Detailed Class Diagram


```mermaid
classDiagram
    %% Base Model (Abstract Class)
    class BaseModel {
        <<Abstract>>
        +String id
        +DateTime createdAt
        +DateTime updatedAt
        +save()
        +update()
        +delete()
        +to_dict()
    }
    
    %% User Entity
    class User {
        +String firstName
        +String lastName
        +String email
        +String password
        +Boolean isAdmin
        +register()
        +updateProfile()
        +authenticate()
        +getPlaces()
        +getReviews()
    }
    
    %% Place Entity
    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +addAmenity(Amenity)
        +removeAmenity(Amenity)
        +updatePlace()
        +getReviews()
        +calculateAverageRating()
    }
    
    %% Review Entity
    class Review {
        +Integer rating
        +String comment
        +submitReview()
        +updateReview()
        +validateRating()
    }
    
    %% Amenity Entity
    class Amenity {
        +String name
        +String description
        +updateAmenity()
    }
    
    %% Inheritance Relationships
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    
    %% Association Relationships
    User "1" -- "*" Place : owns
    User "1" -- "*" Review : writes
    Place "1" -- "*" Review : has
    Place "*" -- "*" Amenity : contains
    
    %% Composition/Strong Relationship
    User "*" --> "1" Place : owns (composition)
    
    %% Aggregation/Weak Relationship
    Place "*" o-- "*" Amenity : has amenities (aggregation)
