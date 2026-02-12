# HBNB Enhanced System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Web[Web Browser]
        Mobile[Mobile App]
        API_Client[API Clients]
    end

    subgraph "Load Balancer"
        LB[NGINX Load Balancer]
    end

    subgraph "Application Layer"
        subgraph "Web Servers"
            WS1[Gunicorn Worker 1]
            WS2[Gunicorn Worker 2]
            WS3[Gunicorn Worker 3]
        end
        
        subgraph "Flask Application"
            API[API Routes]
            Auth[Authentication]
            Cache[Cache Layer]
            WS[WebSocket Server]
        end
    end

    subgraph "Service Layer"
        subgraph "Background Workers"
            Celery[Celery Worker]
            Beat[Celery Beat]
        end
        
        subgraph "Message Queue"
            RabbitMQ[RabbitMQ]
        end
        
        Email[Email Service]
        SMS[SMS Service]
    end

    subgraph "Data Layer"
        subgraph "Primary Database"
            MySQL[(MySQL Master)]
        end
        
        subgraph "Read Replicas"
            MySQL_R1[(MySQL Replica 1)]
            MySQL_R2[(MySQL Replica 2)]
        end
        
        subgraph "Caching"
            Redis_Cache[(Redis Cache)]
            Redis_PubSub[(Redis Pub/Sub)]
        end
        
        subgraph "Object Storage"
            S3[S3-Compatible Storage]
        end
        
        subgraph "Monitoring"
            ELK[ELK Stack]
            Prometheus[Prometheus]
            Grafana[Grafana]
        end
    end

    Web --> LB
    Mobile --> LB
    API_Client --> LB
    LB --> WS1
    LB --> WS2
    LB --> WS3
    WS1 --> API
    WS2 --> API
    WS3 --> API
    API --> Auth
    API --> Cache
    API --> WS
    Cache --> Redis_Cache
    WS --> Redis_PubSub
    API --> MySQL
    API --> MySQL_R1
    Auth --> MySQL
    Celery --> RabbitMQ
    Beat --> RabbitMQ
    Celery --> Email
    Celery --> SMS
    Celery --> MySQL
    API --> S3
    Prometheus --> WS1
    Prometheus --> WS2
    Prometheus --> WS3
    Prometheus --> MySQL
    Prometheus --> Redis_Cache
    Grafana --> Prometheus
    ELK --> WS1
    ELK --> WS2
    ELK --> WS3

    style Web fill:#e1f5fe
    style Mobile fill:#e1f5fe
    style API_Client fill:#e1f5fe
    style LB fill:#fff3e0
    style WS1 fill:#f3e5f5
    style WS2 fill:#f3e5f5
    style WS3 fill:#f3e5f5
    style MySQL fill:#e8f5e8
    style Redis_Cache fill:#fff8e1
    style S3 fill:#fce4ec
Components Description
1. Client Layer
Web Browser: Responsive web interface

Mobile App: Native iOS/Android applications

API Clients: Third-party integrations

2. Load Balancer (NGINX)
SSL termination

Request routing

Static file serving

Rate limiting

IP whitelisting

3. Application Layer
Gunicorn Workers: WSGI HTTP server

Flask Application:

API Routes: RESTful endpoints

Authentication: JWT-based auth

Cache Layer: Redis integration

WebSocket Server: Real-time features

4. Service Layer
Celery Workers: Background task processing

RabbitMQ: Message queue for task distribution

Email Service: Transactional emails

SMS Service: Notifications and alerts

5. Data Layer
MySQL Master: Primary database with write operations

MySQL Replicas: Read-only replicas for scaling reads

Redis Cache: Session storage, caching, rate limiting

Redis Pub/Sub: Real-time messaging

S3 Storage: Media files, backups

6. Monitoring
ELK Stack: Log aggregation and analysis

Prometheus: Metrics collection

Grafana: Dashboard and visualization

Data Flow
Client requests enter through Load Balancer

Requests are distributed to available Gunicorn workers

Flask application processes requests with middleware

Database operations use read replicas when possible

Cache is checked before database queries

Background tasks are queued in RabbitMQ

Real-time updates use WebSocket connections

Metrics and logs are sent to monitoring stack

Scaling Strategy
Horizontal Scaling: Add more application servers

Read Scaling: Add database replicas

Cache Scaling: Redis cluster

Async Processing: Celery workers auto-scaling
