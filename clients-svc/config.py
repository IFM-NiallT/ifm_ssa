import configparser
import os
from dataclasses import dataclass

CONFIG_PATH = os.getenv('CONFIG_PATH', 'config/default.ini')

@dataclass
class ClientsConfig:
    """
    Configuration class for the Clients service.
    
    This class manages the configuration settings for the Clients service,
    including service settings, catalog connection details, and logging configuration.
    
    Attributes:
        host (str): Host address for the service.
        port (int): Port number for the service.
        debug (bool): Debug mode flag.
        log_level (str): Logging level.
        catalog_host (str): Host address for the catalog service.
        catalog_port (int): Port number for the catalog service.
        log_file (str): Path to the log file.
        max_log_size (int): Maximum size of log file before rotation.
        log_backup_count (int): Number of backup log files to keep.
        request_timeout (int): Timeout for HTTP requests in seconds.
    """
    
    # Service settings
    host: str
    port: int
    debug: bool
    log_level: str
    
    # Catalog settings
    catalog_host: str
    catalog_port: int
    
    # Logging settings
    log_file: str = "clients_service.log"
    max_log_size: int = 10000000  # 10MB
    log_backup_count: int = 3
    
    # Request settings
    request_timeout: int = 15  # seconds
    
    @property
    def catalog_url(self) -> str:
        """
        Get the complete catalog service URL.
        
        Returns:
            str: The fully formatted catalog service URL.
        """
        return f"http://{self.catalog_host}:{self.catalog_port}"
    
    @classmethod
    def load_config(cls) -> 'ClientsConfig':
        """
        Load configuration from the config file.
        
        Returns:
            ClientsConfig: Configuration instance with loaded settings.
            
        Raises:
            FileNotFoundError: If the config file is not found.
            configparser.Error: If there's an error parsing the config file.
        """
        config = configparser.ConfigParser()
        
        if not os.path.isfile(CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
            
        config.read(CONFIG_PATH)
        
        return cls(
            host=config.get('service', 'host'),
            port=config.getint('service', 'port'),
            debug=config.getboolean('DEFAULT', 'debug'),
            log_level=config.get('DEFAULT', 'log_level'),
            catalog_host=config.get('catalog', 'host'),
            catalog_port=config.getint('catalog', 'port')
        )