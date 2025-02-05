from flask import Flask, jsonify, Response
import logging
from typing import Tuple, Any
from config import *
from prospects_service import ProspectsService
from exceptions import ProspectServiceError, CatalogServiceError, ProspectDataError

class ProspectsApp:
    """
    Flask application for serving prospect data.
    
    This class initializes and manages the Flask application that serves
    the prospect data API endpoints.
    
    Attributes:
        config (ProspectsServiceConfig): Application configuration.
        app (Flask): Flask application instance.
        service (ProspectsService): Prospects service instance.
        logger (logging.Logger): Application logger.
    """

    def __init__(self):
        """Initialize the Flask application and its components."""
        self.config = ProspectsConfig.load_config()
        self.app = Flask(__name__)
        self.service = ProspectsService(self.config)
        self.logger = self._setup_logger()
        self._setup_routes()
        
        self.logger.info(
            f"Prospects service initialized with config: "
            f"catalog_url={self.config.catalog_url}"
        )

    def _setup_logger(self) -> logging.Logger:
        """
        Set up application logging.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("ProspectsApp")
        logger.setLevel(getattr(logging, self.config.log_level))
        
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def _setup_routes(self) -> None:
        """
        Set up the application routes.
        
        Configures URL routes and maps them to their handler methods.
        """
        self.app.add_url_rule(
            '/get-prospects',
            'get_prospects',
            self._get_prospects,
            methods=['GET']
        )

    def _get_prospects(self) -> Tuple[Response, int]:
        """
        Handle GET requests for prospect data.
        
        Returns:
            Tuple[Response, int]: JSON response and HTTP status code.
        """
        self.logger.info("Received request for prospect data")
        
        try:
            prospect_data = self.service.fetch_prospect_data()
            return jsonify(prospect_data), 200
            
        except CatalogServiceError as e:
            self.logger.error(f"Catalog service error: {str(e)}")
            return jsonify({
                "error": "Unable to fetch prospect data",
                "message": str(e)
            }), 503
            
        except ProspectDataError as e:
            self.logger.error(f"Prospect data error: {str(e)}")
            return jsonify({
                "error": "Invalid prospect data",
                "message": str(e)
            }), 422
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return jsonify({
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }), 500

    def run(self) -> None:
        """
        Run the Flask application.
        
        Starts the Flask server with the configured host and port settings.
        """
        self.logger.info(
            f"Starting ProspectsApp on {self.config.host}:{self.config.port}"
        )
        self.app.run(
            host=self.config.host,
            port=self.config.port,
            debug=self.config.debug
        )

# Application entry points
if __name__ == '__main__':
    app_instance = ProspectsApp()
    app_instance.run()
else:
    # WSGI callable for Gunicorn
    application = ProspectsApp().app