from flask import Flask, jsonify, Response
import logging
from typing import Tuple
from config import ClientsConfig
from clients_service import ClientsService
from exceptions import ClientServiceError, CatalogServiceError, ClientDataError

class ClientsApp:
    """
    Flask application for serving client data.
    
    This class initializes and manages the Flask application that serves
    the client data API endpoints.
    
    Attributes:
        config (ClientsConfig): Application configuration.
        app (Flask): Flask application instance.
        service (ClientsService): Clients service instance.
        logger (logging.Logger): Application logger.
    """

    def __init__(self):
        """Initialize the Flask application and its components."""
        self.config = ClientsConfig.load_config()
        self.app = Flask(__name__)
        self.service = ClientsService(self.config)
        self.logger = self._setup_logger()
        self._setup_routes()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up application logging.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("ClientsApp")
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
            '/get-clients',
            'get_clients',
            self._get_clients,
            methods=['GET']
        )

    def _get_clients(self) -> Tuple[Response, int]:
        """
        Handle GET requests for client data.
        
        Returns:
            Tuple[Response, int]: JSON response and HTTP status code.
        """
        self.logger.info("Received request for client data")
        
        try:
            client_data = self.service.fetch_client_data()
            return jsonify(client_data), 200
            
        except CatalogServiceError as e:
            self.logger.error(f"Catalog service error: {str(e)}")
            return jsonify({
                "error": "Unable to fetch client data",
                "message": str(e)
            }), 503
            
        except ClientDataError as e:
            self.logger.error(f"Client data error: {str(e)}")
            return jsonify({
                "error": "Invalid client data",
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
            f"Starting ClientsApp on {self.config.host}:{self.config.port}"
        )
        self.app.run(
            host=self.config.host,
            port=self.config.port,
            debug=self.config.debug
        )

# Application entry points
if __name__ == '__main__':
    app_instance = ClientsApp()
    app_instance.run()
else:
    # WSGI callable for Gunicorn
    application = ClientsApp().app
