"""Contains the BasePage class which is the parent class for all page objects in the project."""
import copy
import datetime
from abc import ABC
from typing import Any

from t_page_object.selenium_manager import SeleniumManager


class BasePage(ABC):
    """Base page class for all page objects in the project."""

    browser = None
    url = None
    verification_element = None

    def __init__(self):
        """Base Page."""
        self.browser = SeleniumManager.get_instance()

    def __deepcopy__(self, memo: Any):
        """Custom deepcopy to avoid copying the Selenium browser instance."""
        new_copy = copy.copy(self)  # Perform shallow copy
        new_copy.browser = self.browser  # Prevent deep copying the Selenium instance
        return new_copy

    def visit(self) -> None:
        """Navigate to the base page URL."""
        self.browser.go_to(self.url)
        self.wait_page_load()

    def wait_page_load(self) -> None:
        """Wait for the page to load by waiting for the verification element to load."""
        self.verification_element.wait_element_load()

    def wait_for_new_window_and_switch(self, old_window_handles: list) -> None:
        """Function for waiting and switching to new window."""
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=30)
        while datetime.datetime.now() < timeout:
            currents_window_handles = self.browser.get_window_handles()
            if len(currents_window_handles) > len(old_window_handles):
                window = [window for window in currents_window_handles if window not in old_window_handles][0]
                return self.browser.switch_window(window)
        else:
            raise TimeoutError("New window was not opened")
