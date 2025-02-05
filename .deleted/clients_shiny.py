import shiny
from shiny import ui, render, reactive
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ClientsShiny")

# Default catalog service URL
CATALOG_SERVICE_URL = "http://localhost:5000"

class ClientsShinyApp:
    """Shiny app for displaying client details and visit status."""

    def __init__(self):
        """Initialize the Shiny app."""
        self.app_ui = ui.page_fluid(
            ui.h2("Client Details"),
            ui.output_ui("clients_table"),
        )
        self.app = shiny.App(self.app_ui, self.server)

    def server(self, input, output, session):
        """Server logic for the Shiny app."""
        
        # Reactive data store
        client_data = reactive.Value([])

        @reactive.effect
        def fetch_client_data():
            """Fetch client data from the catalog service."""
            try:
                logger.info("Requesting client data from catalog service.")
                response = requests.get(f"{CATALOG_SERVICE_URL}/get-clients", timeout=10)
                response.raise_for_status()
                clients = response.json().get('clients', [])
                client_data.set(clients)
                logger.info(f"Successfully fetched {len(clients)} clients.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching client data: {e}")
                client_data.set([])

        @output
        @render.ui
        def clients_table():
            clients = client_data.get()
            
            if not clients:
                return ui.div("No client data available.")
            
            client_rows = []
            for client in clients:
                client_rows.append(
                    ui.div(
                        ui.h3(client.get("name", "Unknown")),
                        ui.p(f"Address: {client.get('address', 'N/A')}"),
                        ui.p(f"Sales Analysis: {client.get('sales_analysis', 'No Data')}"),
                        ui.p(f"Visit Status: {client.get('visit_status', 'No Data')}"),
                        ui.a("View on Google Maps", href=f"https://www.google.com/maps?q={client.get('address', '')}", target="_blank")
                    )
                )
            return ui.div(*client_rows)

    def run(self):
        """Run the Shiny app."""
        logger.info("Starting Clients Shiny app.")
        self.app.run(host="0.0.0.0", port=8001)

if __name__ == "__main__":
    app = ClientsShinyApp()
    app.run()
