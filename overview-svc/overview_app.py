from flask import Flask, jsonify
from overview_service import OverviewService
import logging

# Initialize Flask and OverviewService
app = Flask(__name__)
service = OverviewService()

# Configure logging
logging.basicConfig(level=logging.INFO)  # Default log level

@app.route('/get-overview', methods=['GET'])
def get_overview():
    """Endpoint to get the sales overview."""
    try:
        app.logger.info("Request received for sales overview.")
        overview_data = service.get_overview()
        return jsonify(overview_data), 200
    except Exception as e:
        app.logger.error(f"Error while fetching overview: {e}")
        return jsonify({"error": "Failed to fetch overview"}), 500

if __name__ == '__main__':
    # Default host and port
    app.run(debug=False, host="0.0.0.0", port=5000)
