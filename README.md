# Sales Support Assistant (SSA)

## Overview
Sales Support Assistant (SSA) is a web-based application designed to assist sales representatives in the field when interacting with customers. It provides essential data on clients, sales reps, and financials, enabling informed decision-making and efficient sales tracking.

The app follows a **microservice architecture**, with containerized services deployed on **AWS**. Data is sourced from **Intact API** and stored in **RedisDB** for optimized performance.

## Key Features
### 1. Overview Dashboard
- **Revenue Counter**: Tracks monthly sales vs. budget.
- **YTD Sales**: Displays Year-To-Date sales.
- **Daily Sales Target**: Estimated based on a weighted percentage distribution.
- **Automated Data Refresh**: Financial data updates daily from RedisDB.

### 2. Client & Prospect Dashboards
- **Customer Details**: Contact information and address.
- **Visit Status & Traffic Light System** *(Lower Priority)*:
  - Sales reps have **5 weeks** to visit a client.
  - If not visited within **5 weeks**, the traffic light turns **red**.
  - **Refreshes yearly or bi-yearly**.
- **Google Maps Redirection**: Generates a dynamic URL for navigation.

## Technology Stack
- **Frontend**: Shiny for Python *(Interactive web application framework)*
- **Backend**: Python *(Handles API interactions, data processing, and business logic)*
- **Database**: RedisDB (Stores client, sales rep, and financial data)
- **Containerization**: Docker
- **Orchestration**: Kubernetes *(For future high availability)*
- **Hosting**: AWS

## Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Python *(Based on backend choice)*
- Redis
- Kubernetes *(for later deployment)*
