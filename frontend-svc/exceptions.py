class ServiceError(Exception):
    """Base exception class for service-related errors."""
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