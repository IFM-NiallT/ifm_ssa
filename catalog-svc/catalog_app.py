from flask import Flask, jsonify
from catalog_service import CatalogService
import logging
import os

# Initialize Flask and CatalogService
app = Flask(__name__)
catalog_service = CatalogService()

# Configure logging
logging.basicConfig(level=logging.INFO)  # Default log level

@app.route('/catalog', methods=['GET'])
def get_catalog():
    """Endpoint to get the entire catalog."""
    try:
        response, status_code = catalog_service.get_catalog()
        return jsonify(response), status_code
    except Exception as e:
        app.logger.error(f"Error in get_catalog: {e}")
        return jsonify({"error": "Failed to fetch catalog"}), 500

if __name__ == '__main__':
    # Default host and port
    app.run(debug=False, host="0.0.0.0", port=5000)