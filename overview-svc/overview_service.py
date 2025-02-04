import logging
from logging.handlers import RotatingFileHandler

class OverviewService:
    """Handles the logic for fetching and calculating the sales overview."""

    def __init__(self, budget_rev_counter=1_000_000, ytd_sales=450_000):
        """Initialize service with defaults."""
        self.logger = self.setup_logger()
        self.budget_rev_counter = budget_rev_counter
        self.ytd_sales = ytd_sales
        self.logger.info(f"Initialized OverviewService with budget: {self.budget_rev_counter}, YTD Sales: {self.ytd_sales}")

    def setup_logger(self):
        """Set up a rotating file logger."""
        logger = logging.getLogger("OverviewService")
        logger.setLevel(logging.INFO)
        
        # Create a rotating file handler
        handler = RotatingFileHandler("overview_service.log", maxBytes=10_000_000, backupCount=3)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def calculate_daily_target(self):
        """Calculate daily target."""
        self.logger.info("Calculating daily target.")
        if self.ytd_sales and self.budget_rev_counter:
            daily_target = (self.budget_rev_counter - self.ytd_sales) / 30  # Assuming 30 days in a month
            self.logger.info(f"Daily target calculated: {daily_target}")
            return daily_target
        self.logger.warning("Unable to calculate daily target. Missing sales data.")
        return None

    def get_overview(self):
        """Return sales overview data."""
        self.logger.info("Fetching sales overview.")
        daily_target = self.calculate_daily_target()
        return {
            "budget_rev_counter": self.budget_rev_counter,
            "ytd_sales": self.ytd_sales,
            "daily_target": daily_target
        }