from datetime import datetime
from pathlib import Path
import sys

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import get_logger  # noqa: E402


SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
logger = get_logger("tests")


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta Chrome en modo headless.",
    )


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    logger.info("Iniciando navegador Chrome")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    request.node.driver = browser
    yield browser
    logger.info("Cerrando navegador Chrome")
    browser.quit()


def save_failure_screenshot(driver, test_name):
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOTS_DIR / f"{timestamp}_{test_name}.png"
    driver.save_screenshot(str(screenshot_path))
    return screenshot_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    driver = getattr(item, "driver", None)

    if report.when == "call" and report.failed and driver:
        screenshot_path = save_failure_screenshot(driver, item.name)
        logger.error("Test fallido: %s. Screenshot: %s", item.name, screenshot_path)
        report.sections.append(("screenshot", str(screenshot_path)))

        extra = getattr(report, "extras", [])
        extra.append(extras.image(str(screenshot_path)))
        report.extras = extra
