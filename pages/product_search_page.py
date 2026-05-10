from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from utils.selenium_utils import SeleniumUtils


class ProductSearchPage:
    # =====================================================
    # Locators — Search Bar
    # =====================================================

    _SEARCH_BUTTON = (By.XPATH, "//summary[@aria-label='Search']")
    _SEARCH_INPUT_BOX = (By.XPATH, "//input[@id='Search-In-Modal']")

    # =====================================================
    # Locators — Search Results
    # =====================================================

    _RESULT_TEXT_XPATH = (By.XPATH, "//p[contains(text(),'found for')]")
    _NO_RESULTS_TEXT_XPATH = (By.XPATH, "//p[contains(text(),'No results found for')]")

    # =====================================================
    # Locators — Product Links (dynamic — string templates)
    # =====================================================

    _PRODUCT_LINK_XPATH = (By.XPATH, "//a[@class='full-unstyled-link']")
    _PRODUCT_LINK_BY_NAME_XPATH = "//a[@class='full-unstyled-link' and contains(normalize-space(.), '{}')]"

    # =====================================================
    # Expected Message Templates
    # =====================================================

    RESULT_FOUND_MSG_FRAGMENT = "found for \u201c{product}\u201d"
    EXPECTED_NO_RESULT_FOUND_MSG = "No results found for \u201c{product}\u201d. Check the spelling or use a different word or phrase."

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self, driver):
        self.driver = driver
        self.sele_utils = SeleniumUtils(self.driver)

    # =====================================================
    # Locator Builder Methods
    # =====================================================

    def get_product_link_by_name_locator(self, product_name: str) -> tuple:
        """
        Builds the product link locator for a specific product name.

        Args:
            product_name: The product name to build the locator for.

        Returns:
            Tuple locator for the specific product link.
        """
        return (By.XPATH, self._PRODUCT_LINK_BY_NAME_XPATH.format(product_name))

    # =====================================================
    # Search Actions
    # =====================================================

    def click_search(self) -> None:
        """Clicks the search icon to open the search modal."""
        self.sele_utils.click(self._SEARCH_BUTTON)

    def search_for_product(self, product: str) -> None:
        """
        Types the product name into the search box and submits.

        Args:
            product: The product name to search for.
        """
        self.sele_utils.send_keys(self._SEARCH_INPUT_BOX, product)
        self.sele_utils.press_enter(self._SEARCH_INPUT_BOX)

    def click_product_link(self, product_name: str) -> None:
        """
        Scrolls to the product link matching the given name and clicks it.
        Uses js_click to handle cases where the element may not be interactable.

        Args:
            product_name: The product name to click.
        """
        locator = self.get_product_link_by_name_locator(product_name)
        self.sele_utils.scroll_into_view(locator)
        self.sele_utils.js_click(locator)

    # =====================================================
    # Data Retrieval
    # =====================================================

    def get_result_found_msg(self, product_name: str) -> str:
        """
        Waits for the result message to appear and returns its text.

        Args:
            product_name: The product name used in the search.

        Returns:
            Full result message string from the UI.
        """
        result_found_element = self.sele_utils.wait_until_visible(self._RESULT_TEXT_XPATH)
        return self.sele_utils.get_text(result_found_element)

    def get_no_results_msg(self, product_name: str) -> str:
        """
        Waits for the no-results message to appear and returns its text.

        Args:
            product_name: The product name used in the search.

        Returns:
            Full no-results message string from the UI.
        """
        no_result_found_element = self.sele_utils.wait_until_visible(self._NO_RESULTS_TEXT_XPATH)
        return self.sele_utils.get_text(no_result_found_element)

    def expected_no_results_found_msg(self, product_name: str) -> str:
        """
        Builds the expected no-results message for a given product name.

        Args:
            product_name: The product name used in the search.

        Returns:
            Formatted expected no-results message string.
        """
        return self.EXPECTED_NO_RESULT_FOUND_MSG.format(product=product_name)

    # =====================================================
    # Validation Methods
    # =====================================================

    def validate_result_found_msg(self, product_name: str, actual_text: str) -> None:
        """
        Asserts that the result message contains the expected product name fragment.
        Count prefix (e.g. '1', '2') is dynamic and excluded from assertion.

        Args:
            product_name: The product name used in the search.
            actual_text:  The full result message retrieved from the UI.
        """
        expected_fragment = self.RESULT_FOUND_MSG_FRAGMENT.format(product=product_name)
        assert expected_fragment in actual_text, (
            f"Result message fragment not found.\n"
            f"  Expected fragment : {expected_fragment}\n"
            f"  Actual message    : {actual_text}"
        )

    def validate_no_results_msg(self, actual: str, expected: str) -> None:
        """
        Asserts that the actual no-results message matches the expected message exactly.

        Args:
            actual:   The full message text retrieved from the UI.
            expected: The expected message text to assert against.
        """
        assert actual == expected, (
            f"No-results message mismatch.\n"
            f"  Expected : {expected}\n"
            f"  Actual   : {actual}"
        )

    def validate_presence_of_product_in_product_link(self, product_name: str) -> None:
        """
        Validates that at least one product link in the search results contains the product name.
        Comparison is case-insensitive to support case-sensitivity test scenarios.

        Args:
            product_name: The product name expected to appear in product links.
        """
        try:
            product_links = self.sele_utils.find_elements(self._PRODUCT_LINK_XPATH)
        except TimeoutException:
            product_links = []

        is_presence = 0
        for product_link in product_links:
            self.sele_utils.scroll_into_view_element(product_link)
            text = self.sele_utils.get_text(product_link)
            if product_name.lower() in text.lower():
                is_presence += 1

        assert is_presence > 0, (
            f"Product '{product_name}' was not found in any product links on the search results page."
        )

    def validate_search_result(self, product_name: str) -> None:
        """
        Retrieves the result message from the UI and validates it contains the product name.

        Args:
            product_name: The product name used in the search.
        """
        actual_result_found_msg = self.get_result_found_msg(product_name)
        self.validate_result_found_msg(product_name, actual_result_found_msg)


    def validate_no_search_result(self, product_name: str) -> None:
        """
        Retrieves the no-results message from the UI and validates it against the expected message.

        Args:
            product_name: The product name used in the search.
            :param self:
        """
        actual_no_result_found_msg = self.get_no_results_msg(product_name)
        expected = self.expected_no_results_found_msg(product_name)
        self.validate_no_results_msg(actual_no_result_found_msg, expected)
