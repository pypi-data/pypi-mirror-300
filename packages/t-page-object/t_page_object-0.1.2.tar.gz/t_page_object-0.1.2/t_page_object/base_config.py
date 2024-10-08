"""Set up the base configuration for the selenium browser."""
from t_object import ThoughtfulObject


class BaseConfig(ThoughtfulObject):
    """
    Stores all Selenium browser configuration variables.

    Attributes:
        make_screenshot (bool): Whether to take screenshots during tests. Defaults to True.
        headless (bool): Whether to run the browser in headless mode (without a GUI). Defaults to False.
        wait_time (int): The default wait time in seconds for browser operations. Defaults to 10.
    """

    make_screenshot: bool = True
    headless: bool = False
    wait_time: int = 10
