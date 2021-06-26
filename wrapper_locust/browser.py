# pylint:disable=too-few-public-methods
import logging
from locust import User

from wrapper_locust import browser_factory
from wrapper_locust.browser_client import BrowserClient

_LOGGER = logging.getLogger(__name__)


class UserWrapper(User):
    """
    this is a wrapper class on User class [previously known as Locust], This class shouldn't directly inherited by
    the Class used for Testing
    """
    client = None
    #   browser_type needs to be override in Testing class
    browser_type = ""
    timeout = 30
    screen_width = None
    screen_height = None

    def __init__(self, environment):
        super(UserWrapper, self).__init__(environment)


class Browser(UserWrapper):
    """
    Any Testing class need to inherit this class to work on Locust
    """

    def __init__(self, environment):
        super(UserWrapper, self).__init__(environment)
        self.client = BrowserClient(
            browser_factory.get_browser(self.browser_type.lower()),
            self.timeout
        )
