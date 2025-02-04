import logging
import requests
from logging.handlers import RotatingFileHandler

class ClientsService:
    """Handles interactions with the clients' data (from the catalog service)."""

    def __init__(self, catalog_service_url="http://localhost:5000", timeout=15):
        """Initialize with catalog service URL and timeout duration."""
        self.logger = self.setup_logger()
        self.catalog_service_url = catalog_service_url
        self.timeout = timeout
        self.logger.info(f"Initialized ClientsService with catalog service URL: {self.catalog_service_url}")

    def setup_logger(self):
        """Set up a rotating file logger."""
        logger = logging.getLogger("ClientsService")
        logger.setLevel(logging.INFO)
        
        # Create a rotating file handler
        handler = RotatingFileHandler("clients_service.log", maxBytes=10_000_000, backupCount=3)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def fetch_client_data(self):
        """Fetch the client data from the catalog service."""
        self.logger.info("Attempting to fetch client data from catalog service...")
        try:
            response = requests.get(f"{self.catalog_service_url}/get-clients", timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Successfully fetched client data from catalog service.")
            return response.json()
        except requests.exceptions.Timeout:
            self.logger.error("Request timed out while fetching client data.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching client data: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        
        return {}  # Return empty data if any error occurs