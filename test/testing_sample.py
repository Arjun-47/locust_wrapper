import time

from locust import task
from selenium.common.exceptions import WebDriverException

from wrapper_locust.browser import Browser
from configparser import ConfigParser

# reading .ini file for configurations for testing purpose
config = ConfigParser()
config.read(r'test\config.ini')


class TestClass(Browser):
    """
    This is a testing class, which inherits the Browser to perform Web UI Automation
    """

    # overrides the browser_type in UserWrapper class
    browser_type = str(config.get('browser_config', 'browser_type'))
    url = str(config.get('browser_config', 'base_url'))

    def __init__(self, environment):
        """
        parameterised constructor, this need to be available in all testing classes
        :param environment: environment argument for User class
        """
        super(TestClass, self).__init__(environment)

    def on_start(self):
        """
        this is a tear_up method which runs once for each instance/user for locust
        :return:
        """
        # sets number users, we are running the automation
        self.client.set_number_of_instances(self.environment.runner.user_count)
        self.client.get(self.url)

    def click_documentation(self):
        self.client.find_element_by_xpath("//a[text()='Documentation']").click()

    def click_edit_in_git(self):
        self.client.find_element_by_xpath("//a[contains(text(), ' Edit on GitHub')]").click()

    def close(self):
        try:
            self.client.close()
            self.client.quit()
        except WebDriverException:
            pass

    @task
    def load_testing(self):
        """
        this method is triggered when we run locust
        :return:
        """
        self.client.event_recorder(self.client, 'Clicking', 'Documentation', self.click_documentation)
        self.client.event_recorder(self.client, 'Clicking', 'Edit in git', self.click_edit_in_git)
        self.close()
        self.client.stop_execution()
        time.sleep(30)
        # locust -f test\testing_sample.py TestClass --headless -u 3 -r 3 --only-summary  --> command to run
