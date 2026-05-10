from selenium.webdriver.common.by import By

from utils.selenium_utils import SeleniumUtils


class LoginPage:

    # =====================================================
    # Locators
    # =====================================================

    _PASSWORD_INPUT = (By.ID,    "password")
    _SUBMIT_BUTTON  = (By.XPATH, "//button[text()='Enter']")

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self, driver):
        self.driver     = driver
        self.sele_utils = SeleniumUtils(driver)

    # =====================================================
    # Actions
    # =====================================================

    def login(self, password: str) -> None:
        """
        Enters the password and clicks the submit button to log in.

        Args:
            password: The password to enter in the password field.
        """
        self.sele_utils.send_keys(self._PASSWORD_INPUT, password)
        self.sele_utils.click(self._SUBMIT_BUTTON)