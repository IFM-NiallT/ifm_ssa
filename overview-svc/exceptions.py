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

class OverviewDataError(DataError):
    """
    Exception raised when there's an error processing overview data.
    
    This exception is raised when there are issues with retrieving or
    processing sales overview data.
    """
    pass

class DataProcessingError(DataError):
    """
    Exception raised when there's an error processing data.
    
    This exception is raised when there are general data processing errors,
    such as calculation errors or data validation failures.
    """
    pass