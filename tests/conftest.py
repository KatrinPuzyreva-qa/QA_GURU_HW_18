import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from attach import add_video, add_console_logs, add_page_source, add_screenshot

# --- ИЗМЕНЕНИЕ 1: Загружаем переменные из конкретного файла .env ---
# Если файл называется stage.env и лежит в корне проекта.
# Если он в подпапке, укажите путь: load_dotenv('path/to/stage.env')
load_dotenv("stage.env")


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to use"
    )
    parser.addoption(
        "--browser_version",
        default="128.0",
        help="Browser version to use"
    )
    # --- ИЗМЕНЕНИЕ 2: Логические значения лучше хранить как булевы ---
    parser.addoption(
        "--headless",
        action="store_true",  # Это автоматически создаст переменную True/False
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--start-url",
        default="https://the-internet.herokuapp.com/login",
        help="URL for test"
    )
    parser.addoption(
        "--selenoid-url",
        default="http://localhost:4444/wd/hub",
        help="URL of Selenoid"
    )
    parser.addoption(
        "--window-size",
        default="1920,1080",
        help="Window Size of Browser"
    )


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    # Получаем логин и пароль из .env файла
    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASSWORD")

    # Получаем параметры из командной строки
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    headless = request.config.getoption("--headless")  # Теперь это True или False
    start_url = request.config.getoption("--start-url")
    selenoid_url = request.config.getoption("--selenoid-url")
    window_size = request.config.getoption("--window-size")

    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument(f"--window-size={window_size}")

    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "name": f"Test_{request.node.name}"  # Имя теста для видео (опционально)
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"{selenoid_url}",  # Просто чистый URL без login:password@
        options=options
    )

    driver.get(start_url)

    yield driver

    # Прикрепляем артефакты к отчету Allure (или другому)
    add_screenshot(driver)
    add_page_source(driver)
    add_console_logs(driver)
    add_video(driver)

    driver.quit()

