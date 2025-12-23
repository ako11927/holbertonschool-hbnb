# Task 0: High-Level Package Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        P1[API]
        P2[Controllers]
        P3[Services]
        P4[DTOs]
    end
    
    subgraph "Business Logic Layer"
        F[HBnB Facade]
        M[Models]
        B[Business Logic]
    end
    
    subgraph "Persistence Layer"
        R[Repository]
        DB[(Database)]
    end
    
    P1 --> F
    P2 --> F
    P3 --> F
    P4 --> F
    F --> M
    F --> B
    B --> R
    R --> DB
    
    style P1 fill:#e1f5fe
    style P2 fill:#e1f5fe
    style P3 fill:#e1f5fe
    style P4 fill:#e1f5fe
    style F fill:#f3e5f5
    style M fill:#f3e5f5
    style B fill:#f3e5f5
    style R fill:#e8f5e8
    style DB fill:#e8f5e8
