#!/bin/bash

echo "Generating HBnB Database Diagrams..."
echo "======================================"

# Create HTML file with interactive diagrams
cat > docs/diagrams.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBnB Database Diagrams</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .diagram { border: 1px solid #ddd; padding: 20px; margin: 20px 0; }
        h1, h2 { color: #333; }
    </style>
    <script>
        mermaid.initialize({startOnLoad:true});
    </script>
</head>
<body>
    <h1>HBnB Database Entity Relationship Diagrams</h1>
    
    <div class="mermaid diagram">
        erDiagram
            USERS {
                string id PK
                string email UK
                string first_name
                string last_name
                boolean is_admin
            }
            
            PLACES {
                string id PK
                string title
                decimal price
                string city
                string owner_id FK
            }
            
            REVIEWS {
                string id PK
                integer rating
                string text
                string user_id FK
                string place_id FK
            }
            
            AMENITIES {
                string id PK
                string name
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
    </div>
    
    <div class="mermaid diagram">
        graph TD
            A[Users] --> B[Places]
            A --> C[Reviews]
            B --> C
            B --> D[Amenities]
            D --> B
            
            style A fill:#bbdefb
            style B fill:#d1c4e9
            style C fill:#c8e6c9
            style D fill:#ffecb3
    </div>
    
    <h2>Data Flow Diagram</h2>
    <div class="mermaid diagram">
        graph TB
            Start[User Registers] --> Create[Create Account]
            Create --> List[List Places]
            List --> View[View Place Details]
            View --> Book[Book Place]
            Book --> Review[Write Review]
            Review --> End[Complete Stay]
            
            Admin[Admin User] --> Manage[Manage System]
            Manage --> Verify[Verify Users]
            Manage --> Monitor[Monitor Reviews]
            Manage --> Update[Update Amenities]
    </div>
</body>
</html>
HTML_EOF

echo "✅ Diagrams generated at: docs/diagrams.html"
echo "Open in browser to view:"
echo "  file://$(pwd)/docs/diagrams.html"
