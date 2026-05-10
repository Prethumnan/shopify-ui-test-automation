# =========================================================
# Test Module  : TestProductSearch
# Description  : Contains all product search related test
#                scenarios for AdNabu Shopify Store
# =========================================================

import pytest

from pages.product_search_page import ProductSearchPage
from utils.data_loader import DataLoader


class TestProductSearch:

    # =====================================================
    # Constants
    # =====================================================

    SEARCH_DATA_FILE           = "product_search.json"

    # JSON keys — positive
    KEY_POSITIVE               = "positive_search_data"
    KEY_EXACT_PRODUCT          = "exact_product_name"
    KEY_PARTIAL_PRODUCT        = "partial_product_name"
    KEY_CASE_SENSITIVE_PRODUCT = "case_sensitive_product_name"

    # JSON keys — negative
    KEY_NEGATIVE               = "negative_search_data"
    KEY_NON_EXISTING_PRODUCT   = "non_existing_product"
    KEY_NUMERIC_INPUT          = "numeric_search_input"
    KEY_COMBINATION_INPUT      = "combination_input"

    # JSON keys — edge case
    KEY_EDGE_CASE              = "edge_case_search_data"
    KEY_XSS_SCRIPT_INPUT       = "xss_script_input"
    KEY_LONG_CHARACTER_INPUT   = "long_character_search"

    # =====================================================
    # Test Data — loaded once at class level
    # =====================================================

    data = DataLoader.load_test_data(SEARCH_DATA_FILE)

    # Positive test data
    exact_product                            = data[KEY_POSITIVE][KEY_EXACT_PRODUCT]
    partial_product                          = data[KEY_POSITIVE][KEY_PARTIAL_PRODUCT]
    case_sensitive_product                   = data[KEY_POSITIVE][KEY_CASE_SENSITIVE_PRODUCT]

    # Negative test data
    invalid_product                          = data[KEY_NEGATIVE][KEY_NON_EXISTING_PRODUCT]
    numeric_input                            = data[KEY_NEGATIVE][KEY_NUMERIC_INPUT]
    combination_of_letter_special_chr_number = data[KEY_NEGATIVE][KEY_COMBINATION_INPUT]

    # Edge case test data
    xss_script_input     = data[KEY_EDGE_CASE][KEY_XSS_SCRIPT_INPUT]
    long_character_input = data[KEY_EDGE_CASE][KEY_LONG_CHARACTER_INPUT]

    # =====================================================
    # Setup Fixture
    # Runs automatically before every test method
    # =====================================================

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Initializes ProductSearchPage before each test.

        Args:
            driver: Selenium WebDriver instance from conftest fixture.
        """
        self.search_page = ProductSearchPage(driver)

    # =====================================================
    # Helper Methods
    # =====================================================

    def _search_and_validate_result(self, product_name: str) -> None:
        """
        Clicks search, types the product name, and validates the result message.

        Args:
            product_name: The product name to search and validate.
        """
        self.search_page.click_search()
        self.search_page.search_for_product(product_name)
        self.search_page.validate_search_result(product_name)

    def _search_and_validate_no_result(self, product_name: str) -> None:
        """
        Clicks search, types the input, and validates the no-results message.

        Args:
            product_name: The search input to validate no results for.
        """
        self.search_page.click_search()
        self.search_page.search_for_product(product_name)
        self.search_page.validate_no_search_result(product_name)

    # =====================================================
    # Positive Test Cases
    # Validates successful product search scenarios
    # =====================================================

    def test_search_exact_product_name(self):
        """
        PS-TC-01 | Positive
        Verify user can search using exact product name and result message reflects it.
        """
        self._search_and_validate_result(self.exact_product)
        self.search_page.validate_presence_of_product_in_product_link(self.exact_product)

    def test_search_partial_product_name(self):
        """
        PS-TC-02 | Positive
        Verify search works with partial product keyword.
        """
        self._search_and_validate_result(self.partial_product)
        self.search_page.validate_presence_of_product_in_product_link(self.partial_product)

    def test_search_case_sensitive_product_name(self):
        """
        PS-TC-03 | Positive
        Verify search works irrespective of text case.
        """
        self._search_and_validate_result(self.case_sensitive_product)
        self.search_page.validate_presence_of_product_in_product_link(self.exact_product)

    # =====================================================
    # Negative Test Cases
    # Validates invalid search scenarios
    # =====================================================

    def test_search_non_existing_product(self):
        """
        PS-TC-04 | Negative
        Verify application handles non-existing product search.
        """
        self._search_and_validate_no_result(self.invalid_product)

    def test_search_using_only_numbers(self):
        """
        PS-TC-05 | Negative
        Verify application handles numeric search input.
        """
        self._search_and_validate_no_result(self.numeric_input)

    def test_search_with_combination_of_letters_strings_special_character(self):
        """
        PS-TC-06 | Negative
        Verify application handles combination of letters, numbers and special characters.
        """
        self._search_and_validate_no_result(self.combination_of_letter_special_chr_number)

    # =====================================================
    # Edge Case Test Cases
    # Validates boundary and abnormal input scenarios
    # =====================================================

    def test_search_with_xss_input(self):
        """
        PS-TC-07 | Edge Case
        Verify application handles XSS script input safely without opening any popup.
        """
        self._search_and_validate_no_result(self.xss_script_input)

    def test_search_with_long_characters(self):
        """
        PS-TC-08 | Edge Case
        Verify application handles very long search input.
        """
        self._search_and_validate_no_result(self.long_character_input)