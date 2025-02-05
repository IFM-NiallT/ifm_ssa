import logging
from typing import Dict, Any, Tuple
from flask import Flask, jsonify
from config import OverviewConfig
from overview_service import OverviewService
from exceptions import OverviewDataError

class OverviewApp:
    """
    Flask application for serving sales overview data.
    
    This class initializes and manages the Flask application that serves
    the sales overview API endpoints. It handles routing, logging, and
    error handling for the overview service.
    
    Attributes:
        config (OverviewConfig): Application configuration.
        app (Flask): Flask application instance.
        service (OverviewService): Overview service instance.
        logger (logging.Logger): Application logger.
    """

    def __init__(self):
        """Initialize the Flask application and its components."""
        self.config = OverviewConfig.load_config()
        self.app = Flask(__name__)
        self.service = OverviewService(self.config)
        self.logger = self._setup_logger()
        self._setup_routes()
        
        self.logger.info(
            f"Overview service initialized with config: "
            f"catalog_url={self.config.catalog_url}"
        )

    def _setup_logger(self) -> logging.Logger:
        """
        Configure logging for the application.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("OverviewApp")
        logger.setLevel(getattr(logging, self.config.log_level))
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
            '/get-overview',
            'get_overview',
            self._get_overview,
            methods=['GET']
        )

    def _get_overview(self) -> Tuple[Dict[str, Any], int]:
        """
        Handle GET requests for overview data.
        
        Returns:
            Tuple[Dict[str, Any], int]: Response data and HTTP status code.
        """
        try:
            self.logger.info("Received request for sales overview")
            overview_data = self.service.get_overview()
            return jsonify(overview_data), 200
            
        except OverviewDataError as e:
            self.logger.error(f"Overview data error: {str(e)}")
            return jsonify({
                "error": "Failed to fetch overview",
                "message": str(e)
            }), 500
            
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
            f"Starting OverviewApp on {self.config.host}:{self.config.port}"
        )
        self.app.run(
            host=self.config.host,
            port=self.config.port,
            debug=self.config.debug
        )

# Application entry points
if __name__ == '__main__':
    app_instance = OverviewApp()
    app_instance.run()
else:
    # WSGI callable for Gunicorn
    application = OverviewApp().app
