
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser


@pytest.fixture(scope='session', autouse=True)
def browser_setup():
    options = Options()
    #options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")

    options.set_capability("goog:loggingPrefs", {
        "browser": "ALL",
        "performance": "ALL"
    })

    driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.timeout = 6
    browser.config.base_url = "https://automationintesting.online/"

    yield
    driver.quit()


# ------------------------
#    FAIL HOOKS
# ------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        try:
            # Screenshot
            png = browser.driver.get_screenshot_as_png()
            allure.attach(png, "screenshot", allure.attachment_type.PNG)

            # Page source
            html = browser.driver.page_source
            allure.attach(html, "page_source", allure.attachment_type.HTML)

            # Browser console logs
            logs = browser.driver.get_log("browser")
            allure.attach(
                "\n".join([str(log) for log in logs]),
                "browser_console",
                allure.attachment_type.TEXT
            )

            # Performance logs
            perf = browser.driver.get_log("performance")
            allure.attach(
                "\n".join([str(entry) for entry in perf]),
                "performance_logs",
                allure.attachment_type.TEXT
            )

        except Exception as e:
            allure.attach(str(e), "ERROR_WHILE_COLLECTING_LOGS", allure.attachment_type.TEXT)
