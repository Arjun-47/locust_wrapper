from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


def chrome():
    return webdriver.Chrome(executable_path=ChromeDriverManager().install())


def ie():
    return webdriver.Ie(executable_path=IEDriverManager().install())


def edge():
    return webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())


def firefox():
    return webdriver.Firefox(executable_path=GeckoDriverManager().install())


def opera():
    return webdriver.Firefox(executable_path=OperaDriverManager().install())


def get_browser(browser_name: str, screen_width=1366, screen_height=768, set_window=True):
    if browser_name == 'chrome':
        driver = chrome()
    elif browser_name == 'edge':
        driver = edge()
    elif browser_name == 'firefox':
        driver = firefox()
    elif browser_name == 'opera':
        driver = opera()
    else:
        driver = ie()
    if set_window:
        driver.set_window_size(screen_width, screen_height)
    return driver
