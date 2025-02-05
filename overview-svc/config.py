import configparser
import os
from dataclasses import dataclass
from typing import ClassVar

CONFIG_PATH = os.getenv('CONFIG_PATH', 'config/default.ini')

@dataclass
class OverviewConfig:
    """
    Configuration class for the Overview service.
    
    This class manages the configuration settings for the Overview service,
    including service settings and catalog connection details.
    
    Attributes:
        host (str): Host address for the service.
        port (int): Port number for the service.
        debug (bool): Debug mode flag.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        catalog_host (str): Host address for the catalog service.
        catalog_port (int): Port number for the catalog service.
    """
    
    # Service settings
    host: str
    port: int
    debug: bool
    log_level: str
    
    # Catalog settings
    catalog_host: str
    catalog_port: int
    
    @property
    def catalog_url(self) -> str:
        """
        Get the complete catalog service URL.
        
        Returns:
            str: The fully formatted catalog service URL.
        """
        return f"http://{self.catalog_host}:{self.catalog_port}"
    
    @classmethod
    def load_config(cls) -> 'OverviewConfig':
        """
        Load configuration from the config file.
        
        Returns:
            OverviewConfig: Configuration instance with loaded settings.
            
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