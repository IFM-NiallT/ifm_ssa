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

class ProspectDataError(ServiceError):
    """
    Exception raised when there's an error processing prospect data.
    
    This exception is raised when there are issues with prospect data structure,
    validation, or processing.
    """
    pass

class ProspectServiceError(ServiceError):
    """
    Exception raised when there's an unexpected error in the prospect service.
    
    This exception is raised for general service-level errors that don't fit
    into more specific categories.
    """
    pass