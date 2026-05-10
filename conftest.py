# =========================================================
# conftest.py
# Special pytest configuration file for reusable fixtures,
# setup/teardown methods, and shared test configurations.
# Pytest automatically detects this file and makes fixtures
# available across the framework without manual imports.
# =========================================================

import configparser
import os

import pytest

from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory


# =====================================================
# Private Helpers
# =====================================================

def _load_config() -> configparser.ConfigParser:
    """
    Loads configuration values from config.ini file.
    Reads browser name, base URL, and credentials.

    Returns:
        ConfigParser object with all config.ini values.
    """
    config      = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "config.ini")
    config.read(config_path)
    return config


# =====================================================
# Session-Scoped Fixtures
# Run once for the entire test session
# =====================================================

@pytest.fixture(scope="session")
def app_config() -> configparser.ConfigParser:
    """
    Loads and shares application configuration across all tests.
    Runs only once per test session to avoid repeated file reads.

    Returns:
        ConfigParser object with all config.ini values.
    """
    return _load_config()


# =====================================================
# Function-Scoped Fixtures
# Run before and after every test function
# =====================================================

@pytest.fixture(scope="function")
def driver(app_config):
    """
    Sets up and tears down the browser for each test.
    Reads browser and base URL from config.ini.

    Args:
        app_config: Session-scoped config fixture.

    Yields:
        WebDriver instance with the application URL open.
    """
    browser  = app_config["settings"]["browser"]
    base_url = app_config["settings"]["base_url"]

    web_driver = DriverFactory.get_driver(browser)
    web_driver.get(base_url)

    yield web_driver

    web_driver.quit()


@pytest.fixture(scope="function", autouse=True)
def setup_login(driver, app_config) -> None:
    """
    Logs into the application before every test.
    Runs automatically — no need to call explicitly in tests.

    Args:
        driver:     WebDriver instance from the driver fixture.
        app_config: Session-scoped config fixture.
    """
    password = app_config["credentials"]["password"]
    login    = LoginPage(driver)
    login.login(password)