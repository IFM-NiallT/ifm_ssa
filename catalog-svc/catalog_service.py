import redis
import json
import logging
from logging.handlers import RotatingFileHandler

class CatalogService:
    """A service class to manage catalog data in Redis."""

    def __init__(self, redis_host="localhost", redis_port=6379):
        """Initialize Redis connection."""
        self.logger = self.setup_logger()
        
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            self.logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        except redis.ConnectionError as e:
            self.logger.error(f"Redis connection error: {e}")
            raise Exception("Failed to connect to Redis") from e

    def setup_logger(self):
        """Set up a rotating file logger."""
        logger = logging.getLogger("CatalogService")
        logger.setLevel(logging.INFO)  # Default log level
        
        # Create a rotating file handler
        handler = RotatingFileHandler("catalog_service.log", maxBytes=10_000_000, backupCount=3)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def get_catalog(self):
        """Retrieve all catalog items from Redis."""
        try:
            data = self.redis_client.hgetall('catalog')
            for key, value in data.items():
                try:
                    data[key] = json.loads(value)  # Convert JSON strings to dict
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to decode JSON for key {key}: {e}")
                    data[key] = {}

            self.logger.info("Fetched catalog successfully.")
            return {"catalog": data}, 200
        except Exception as e:
            self.logger.error(f"Error fetching catalog: {e}")
            return {"error": "Internal Server Error"}, 500
