from flask import Flask, render_template, jsonify
from clients_service import ClientsService
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ClientsApp")

# Initialize Flask app
app = Flask(__name__)

# Initialize the ClientsService with default catalog service URL
clients_service = ClientsService()

@app.route('/')
def index():
    """Display client data including details, sales analysis, visit status, and Google Maps link."""
    logger.info("Rendering client details page")
    client_data = clients_service.fetch_client_data()
    clients = client_data.get('clients', [])
    return render_template('clients.html', clients=clients)

if __name__ == '__main__':
    logger.info("Starting ClientsApp Flask application")
    app.run(debug=False, host="0.0.0.0", port=5001)