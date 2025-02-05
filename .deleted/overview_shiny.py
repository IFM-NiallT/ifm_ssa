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
logger = logging.getLogger("OverviewShiny")

# Default Flask API URL
FLASK_API_URL = "http://localhost:5000"

class OverviewShinyApp:
    """Shiny app for displaying sales overview, fetching data from Flask backend."""

    def __init__(self):
        """Initialize the Shiny app."""
        self.app_ui = ui.page_fluid(
            ui.h2("Sales Overview"),
            ui.output_text("budget_rev_counter"),
            ui.output_text("ytd_sales"),
            ui.output_text("daily_target")
        )
        self.app = shiny.App(self.app_ui, self.server)

    def server(self, input, output, session):
        """Server logic for the Shiny app."""
        
        # Reactive data store
        overview_data = reactive.Value({})

        @reactive.effect
        def fetch_overview_data():
            """Fetch sales overview data from Flask backend."""
            try:
                logger.info("Requesting overview data from Flask API.")
                response = requests.get(f"{FLASK_API_URL}/get-overview", timeout=10)
                response.raise_for_status()
                overview_data.set(response.json())
                logger.info("Successfully fetched overview data.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching data: {e}")
                overview_data.set({"error": str(e)})

        @output
        @render.text
        def budget_rev_counter():
            data = overview_data.get()
            return f"Budget Revenue Counter: ${data.get('budget_rev_counter', 0):,.2f}" if 'error' not in data else f"Error: {data['error']}"

        @output
        @render.text
        def ytd_sales():
            data = overview_data.get()
            return f"Year-to-Date Sales: ${data.get('ytd_sales', 0):,.2f}" if 'error' not in data else f"Error: {data['error']}"

        @output
        @render.text
        def daily_target():
            data = overview_data.get()
            return f"Daily Target: ${data.get('daily_target', 0):,.2f}" if 'error' not in data and data.get('daily_target') is not None else "Daily Target: Not Available"

    def run(self):
        """Run the Shiny app."""
        logger.info("Starting Overview Shiny app.")
        self.app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app = OverviewShinyApp()
    app.run()