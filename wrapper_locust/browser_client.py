# pylint:disable=too-few-public-methods
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from locust import events
from locust.exception import StopUser

num_of_instances = 0
num_instances_completed = 0
num_instances_failed = 0


class BrowserClient(object):

    def __init__(self, driver: webdriver, wait_time_to_finish):
        """
        browser client constructor
        :param driver: instance of the browser
        :param wait_time_to_finish: web driver wait time
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_time_to_finish)

    @staticmethod
    def event_recorder(client, func_type, func_desc, func, *args, **kwargs):
        """
        Use this method whenever you have a logical sequence of browser steps that you would like to time. Group these
        in a separate, not @task method and call them using this method. These will show up in the locust web interface
        with timings

        :param client: Browser instance
        :param func_type: function type, can be duplicate
        :param func_desc: function description, should be unique
        :param func: callable to be timed and logged
        :param args: arguments to be used when calling func
        :param kwargs: Arbitrary keyword args used for calling func
        :return: func(*args, **kwargs) if this function invocation does not raise an exception
        :raise StopUser: whenever func raises an exception, this exception is caught, logged to locust as a failure and
        a StopUser exception is raised.
        """
        global num_instances_failed
        # captures start time
        start_time = time.time()
        try:
            # executes the function passed
            result = func(*args, **kwargs)
        except Exception as event_exception:
            # captures exception occurred time and calculates the execution time
            total_time = int((time.time() - start_time) * 1000)
            # triggers the failure event to locust to capture failed scenario and exception message
            events.request_failure.fire(
                request_type=func_type,
                name=func_desc,
                response_time=total_time,
                response_length=0,
                exception=event_exception
            )
            try:
                # closes the browser after exception event
                client.quit()
            except WebDriverException:
                pass
            # increases the failed instance counter
            num_instances_failed += 1
            # stops execution if number of instances equals to total instances
            if num_of_instances == (num_instances_failed + num_instances_completed):
                exit(0)
            raise StopUser()
        else:
            # captures total execution time to complete the function
            total_time = int((time.time() - start_time) * 1000)
            # triggers the success event to locust to capture passed scenario with execution time
            events.request_success.fire(
                request_type=func_type,
                name=func_desc,
                response_time=total_time,
                response_length=0
            )
            return result

    @staticmethod
    def set_number_of_instances(count):
        """
        this method is to set the number instances that user runs
        :param count: users count
        :return:
        """
        global num_of_instances
        num_of_instances = count

    @staticmethod
    def stop_execution():
        """
        This method increase the counter by 1 when it's called and stops execution if total instances [i.e. passed and
        failed instances]
        :return:
        """
        global num_instances_completed
        num_instances_completed += 1
        if num_of_instances == (num_instances_failed + num_instances_completed):
            exit(0)

    def __getattr__(self, attr):
        """
        Forward all messages this client doesn't understand to it's web driver
        """
        return getattr(self.driver, attr)
