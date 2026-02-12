# Task 2: Sequence Diagrams

## Overview
These sequence diagrams illustrate the flow of 4 key operations in HBnB Evolution, showing interactions between the Presentation, Business Logic, and Persistence layers.

---

## Diagram 1: User Registration

### Description
Shows the complete flow when a new user registers in the system.

```mermaid
sequenceDiagram
    participant User as Client/User
    participant API as API Endpoint
    participant Controller as UserController
    participant Service as UserService
    participant Facade as HBnB Facade
    participant UserModel as User Model
    participant Repo as UserRepository
    participant DB as Database

    User->>API: POST /api/users (user data)
    API->>Controller: routeRequest(userDTO)
    
    Controller->>Service: validateUserData(userDTO)
    Service->>Service: Validate email format, password strength
    Service-->>Controller: Validation result
    
    Controller->>Facade: registerUser(userDTO)
    
    Facade->>UserModel: createUserInstance(userDTO)
    UserModel->>UserModel: generateId(), setTimestamps()
    UserModel->>UserModel: encryptPassword()
    
    Facade->>Repo: save(user)
    Repo->>DB: INSERT INTO users (...)
    DB-->>Repo: Success (new user ID)
    Repo-->>Facade: Saved user object
    
    Facade->>Facade: applyPostRegistrationRules(user)
    
    Facade-->>Controller: Registered user object
    Controller->>Controller: convertToResponseDTO(user)
    Controller-->>API: UserResponseDTO
    API-->>User: HTTP 201 Created + user data
