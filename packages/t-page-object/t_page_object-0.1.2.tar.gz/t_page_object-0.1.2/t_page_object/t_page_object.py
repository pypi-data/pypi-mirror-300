"""Main module."""
from t_page_object.utils.logger import logger


class TPageObject:
    """Base class for page objects."""

    def __init__(self):
        """Initialise the page object."""
        logger.info(f"Instancing {self}")
