class ServiceError(Exception):
    """
    Base exception class for service-level errors.
    
    This is the parent class for all service-specific exceptions in the application.
    """
    pass

class CatalogServiceError(ServiceError):
    """
    Exception raised when there's an error communicating with the catalog service.
    
    This exception is raised when there are connection issues, timeout errors,
    or other problems related to catalog service communication.
    """
    pass

class DataError(ServiceError):
    """
    Base class for data-related errors.
    
    Parent class for all exceptions related to data processing and handling.
    """
    pass

class ClientDataError(DataError):
    """
    Exception raised when there's an error processing client data.
    
    This exception is raised when there are issues with client data structure,
    validation, or processing.
    """
    pass

class ClientServiceError(ServiceError):
    """
    Exception raised when there's an unexpected error in the client service.
    
    This exception is raised for general service-level errors that don't fit
    into more specific categories.
    """
    pass