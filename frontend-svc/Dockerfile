# Use Python slim image for a smaller footprint
# Explicitly use version for stability
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_DIR=/var/log/frontend_service

# Install system dependencies
# Group commands to reduce layers
# Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m -s /bin/bash appuser

# Create log directory and set permissions
RUN mkdir -p ${LOG_DIR} && \
    chown appuser:appuser ${LOG_DIR}

# Copy requirements file separately to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY frontend_app.py .
COPY frontend_service.py .
COPY exceptions.py .
COPY config.py .
COPY config/default.ini ./config/

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Add healthcheck to monitor application status
# Test the health endpoint every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
# Using uvicorn for production-grade server
CMD ["python", "frontend_app.py"]