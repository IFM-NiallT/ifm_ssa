import configparser
import os
from dataclasses import dataclass

CONFIG_PATH = os.getenv('CONFIG_PATH', 'config/default.ini')

@dataclass
class FrontendConfig:
    """
    Configuration class for the Frontend service.
    
    This class manages the configuration settings for the Frontend service,
    including service settings and backend service URLs.
    
    Attributes:
        host (str): Host address for the service.
        port (int): Port number for the service.
        debug (bool): Debug mode flag.
        log_level (str): Logging level.
        refresh_interval (int): Data refresh interval in seconds.
        overview_url (str): URL for the overview service.
        clients_url (str): URL for the clients service.
        prospects_url (str): URL for the prospects service.
    """
    
    # Service settings
    host: str
    port: int
    debug: bool
    log_level: str
    refresh_interval: int
    
    # Backend service URLs
    overview_url: str
    clients_url: str
    prospects_url: str
    
    @classmethod
    def load_config(cls) -> 'FrontendConfig':
        """
        Load configuration from the config file.
        
        Returns:
            FrontendConfig: Configuration instance with loaded settings.
            
        Raises:
            FileNotFoundError: If the config file is not found.
            configparser.Error: If there's an error parsing the config file.
        """
        if not os.path.isfile(CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
            
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        
        return cls(
            host=config.get('service', 'host'),
            port=config.getint('service', 'port'),
            debug=config.getboolean('DEFAULT', 'debug'),
            log_level=config.get('DEFAULT', 'log_level'),
            refresh_interval=config.getint('DEFAULT', 'refresh_interval'),
            overview_url=config.get('backend_services', 'overview_url'),
            clients_url=config.get('backend_services', 'clients_url'),
            prospects_url=config.get('backend_services', 'prospects_url')
        )