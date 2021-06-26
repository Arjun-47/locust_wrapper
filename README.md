# Locust wrapper for browser with Locust load testing

This python package provides different Locusts that represent real browsers. This package is a thin wrapper around (parts of) Selenium Webdriver.


Installation via pip

    pip install locust_wrapper

Once installed, simple make a testing_sample.py as per usual, but instead of inheriting your locust from HttpUser, instantiate a Browser.

This locust expose a self.client object, that is actually a selenium.webdriver, it will understand all the usual methods. The client also exposes a self.client.wait object, that is a selenium's WebDriverWait. A last method that is exposed by the client is the self.client.event_recorder method, that can be used to group a number of browser actions together, and time them in locust.

An example locust scenario that uses real browser could be:

```python
import time

from locust import task
from selenium.common.exceptions import WebDriverException

from wrapper_locust.browser import Browser


class TestClass(Browser):

    browser_type = 'chrome'
    url = 'https://locust.io/'

    def __init__(self, environment):
        super(TestClass, self).__init__(environment)

    def on_start(self):
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
        self.client.event_recorder(self.client, 'Clicking', 'Documentation', self.click_documentation)
        self.client.event_recorder(self.client, 'Clicking', 'Edit in git', self.click_edit_in_git)
        self.close()
        self.client.stop_execution()
        time.sleep(30)
        # locust -f test\testing_sample.py TestClass --headless -u 3 -r 3 --only-summary  --> command to run

```

## Run locust

### Running Locust with Web UI

```commandline
locust -f package\python_file.py PythonClass
```

### Running Locust Without Web UI

```commandline
locust -f package\python_file.py PythonClass --headless -u NUM_USERS -r HATCH_RATE
```

### Running Locust without Web UI and only summary

```commandline
locust -f package\python_file.py PythonClass --headless -u NUM_USERS -r HATCH_RATE --only-summary
```

### Running Locust without Web UI, csv file output, logfile and only summary option

```commandline
locust -f package\python_file.py PythonClass --headless -u NUM_USERS -r HATCH_RATE --only-summary --csv CSV_FILE_NAME --logfile LOG_FILE_NAME
```

### Running Locust without Web UI and html report

```commandline
locust -f package\python_file.py PythonClass --headless -u NUM_USERS -r HATCH_RATE --html HTML_FILE_NAME
```
