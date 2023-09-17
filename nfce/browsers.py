from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def get_chrome_browser():
    options = ChromeOptions()
    options.add_argument("--headless")

    service = ChromeService(ChromeDriverManager().install())
    browser = Chrome(service=service, options=options)

    return browser

def get_edge_browser():
    options = EdgeOptions()
    options.add_argument("--headless")

    service = EdgeService(EdgeChromiumDriverManager().install())
    browser = Edge(service=service, options=options)

    return browser

def get_firefox_browser():
    options = FirefoxOptions()
    options.add_argument("--headless")

    service = FirefoxService(GeckoDriverManager().install())
    browser = Firefox(service=service, options=options)

    return browser
