# Technical Documentation

## Overview
Sales Support Assistant (SSA) is a web-based application designed to assist sales representatives in the field when interacting with customers. It provides essential data on clients, sales reps, and financials, enabling informed decision-making and efficient sales tracking.

The app follows a **microservice architecture**, with containerized services deployed on **AWS**. Data is sourced from **PostgreSQL**, ensuring robust data persistence and relational integrity.

## System Design

### Architecture Overview
The SSA implements a microservices architecture where:
- Each service is independently deployable
- Backend services retrieve data through the catalog service
- Each service handles its own error states
- Services provide health check endpoints
- Future logging will be handled through ELK stack (Elasticsearch, Fluentbit, Kibana)

### Service Details

#### Gateway Service (gateway-svc)
- Nginx-based reverse proxy
- Routes traffic to frontend service
- Features:
  - WebSocket support for Shiny
  - Gzip compression
  - Custom error pages
  - Health check endpoint

#### Frontend Service (frontend-svc)
- Built with Shiny for Python
- Features:
  - Service status indicators
  - Daily data refresh display
  - Error state handling
  - Progress indicators

#### Backend Services

##### Overview Service (overview-svc)
- Sales metrics handler
- Features:
  - Daily budget tracking
  - YTD calculations
  - Daily target computations based on refreshed data
  - Data refreshed daily from previous day's sales

##### Clients Service (clients-svc)
- Client relationship management
- Features:
  - Contact information management
  - Location data
  - Traffic light monitoring system for visits
    - Monitors visit frequency (feature in development)
  - Google Maps integration (planned)
    - One-click redirect to client location
  - Sales analysis (planned feature)

##### Prospects Service (prospects-svc)
- Prospect management
- Features:
  - Contact information management
  - Location data
  - Traffic light monitoring system for visits
    - Monitors visit frequency (feature in development)
  - Google Maps integration (planned)
    - One-click redirect to prospect location

##### Catalog Service (catalog-svc)
- Central data handler
- Features:
  - PostgreSQL integration
  - Data provision to other services
  - Data validation
  - Central point for database interactions

## Technical Implementation

### Error Handling
Services implement a standardized error handling approach:

```python
class ServiceError(Exception):
    """Base exception for service errors."""
    pass

class ServiceTimeoutError(ServiceError):
    """Raised when a service request times out."""
    pass

class ServiceUnavailableError(ServiceError):
    """Raised when a service is unavailable."""
    pass

class ConfigurationError(ServiceError):
    """Raised when there's an error in configuration."""
    pass
```

Error responses follow a standard format:
```python
{
    "error": "Error type description",
    "message": "Detailed error message",
    "details": "Additional error context"
}
```

### Logging
Current logging implementation with planned ELK stack integration:
```python
# Current implementation
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("service.log")
    ]
)

# Rotating file handler for log management
file_handler = RotatingFileHandler(
    'service.log',
    maxBytes=10000000,  # 10MB
    backupCount=3
)
```

Future logging will be handled by:
- Elasticsearch: Log storage and search
- Fluentbit: Log collection and forwarding
- Kibana: Log visualization and analysis

## Future Deployment Plans:

### AWS Deployment (planned, subject to change)
Components:
- ECS for container orchestration
- ECR for container registry
- RDS for PostgreSQL
- ALB for load balancing
- CloudWatch for monitoring

### Kubernetes Deployment (planned, subject to change)
Components:
- Service deployments
- Ingress controllers
- ConfigMaps and Secrets
- Persistent volumes
- Horizontal pod autoscaling

## Authors
- Industrial and Farm Machinary LTD.
- Luke Doyle (Intern 2025)