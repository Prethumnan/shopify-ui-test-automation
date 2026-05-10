# =========================================================
# Test Module  : TestAddToCart
# Description  : Contains all add to cart related test
#                scenarios for AdNabu Shopify Store
# =========================================================

import pytest

from pages.add_to_cart_page import AddToCartPage
from pages.product_search_page import ProductSearchPage
from utils.data_loader import DataLoader
import time


class TestAddToCart:

    # =====================================================
    # Constants
    # =====================================================

    CART_DATA_FILE                  = "add_to_cart.json"

    # JSON keys — positive
    KEY_POSITIVE                    = "positive_cart_data"
    KEY_SINGLE_PRODUCT              = "single_product_name"

    # JSON keys — negative
    KEY_NEGATIVE                    = "negative_cart_data"
    KEY_OUT_OF_STOCK_PRODUCT        = "out_of_stock_product"
    KEY_MINIMUM_QUANTITY_PRODUCT    = "minimum_quantity_product"

    # =====================================================
    # Test Data — loaded once at class level
    # =====================================================

    data = DataLoader.load_test_data(CART_DATA_FILE)

    # Positive test data
    single_product           = data[KEY_POSITIVE][KEY_SINGLE_PRODUCT]

    # Negative test data
    out_of_stock_product     = data[KEY_NEGATIVE][KEY_OUT_OF_STOCK_PRODUCT]
    minimum_quantity_product = data[KEY_NEGATIVE][KEY_MINIMUM_QUANTITY_PRODUCT]

    # =====================================================
    # Setup Fixture
    # Runs automatically before every test method
    # =====================================================

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Initializes page objects before each test.

        Args:
            driver: Selenium WebDriver instance from conftest fixture.
        """
        self.cart_page   = AddToCartPage(driver)
        self.search_page = ProductSearchPage(driver)

    # =====================================================
    # Helper Methods
    # =====================================================

    def _search_and_open_product(self, product_name: str) -> None:
        """
        Searches for a product and navigates to its product page.

        Args:
            product_name: The product name to search and open.
        """
        self.search_page.click_search()
        self.search_page.search_for_product(product_name)
        self.search_page.click_product_link(product_name)

    def _search_and_add_to_cart(self, product_name: str) -> None:
        """
        Searches for a product, opens its page, and adds it to the cart.

        Args:
            product_name: The product name to add to cart.
        """
        self._search_and_open_product(product_name)
        self.cart_page.click_add_to_cart()

    def _validate_item_total_and_subtotal(self, unit_price: float, quantity: int) -> None:
        """
        Validates that item total equals unit price × quantity,
        and that item total matches the cart subtotal.

        Args:
            unit_price: The unit price of the product.
            quantity:   The current quantity in the cart.
        """
        item_total     = self.cart_page.get_cart_item_total(expected_min_value=unit_price)
        subtotal       = self.cart_page.get_cart_subtotal()
        expected_total = round(unit_price * quantity, 2)

        assert item_total == expected_total, (
            f"Item total '{item_total}' does not match "
            f"unit price '{unit_price}' × quantity '{quantity}' = '{expected_total}'."
        )
        assert item_total == subtotal, (
            f"Item total '{item_total}' does not match subtotal '{subtotal}'."
        )

    # =====================================================
    # Positive Test Cases
    # Validates successful add to cart scenarios
    # =====================================================

    def test_increase_quantity_reflects_in_item_total_and_subtotal(self):
        """Verify that after clicking plus, item total and subtotal are equal."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        unit_price = self.cart_page.get_cart_item_unit_price()
        self.cart_page.click_plus_button(self.minimum_quantity_product)
        quantity   = self.cart_page.get_cart_item_quantity()
        self._validate_item_total_and_subtotal(unit_price, quantity)

    def test_increase_quantity_reflects_correct_calculation(self):
        """Verify item total equals unit price multiplied by quantity after clicking plus."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        unit_price = self.cart_page.get_cart_item_unit_price()
        self.cart_page.click_plus_button(self.minimum_quantity_product)
        quantity   = self.cart_page.get_cart_item_quantity()
        self._validate_item_total_and_subtotal(unit_price, quantity)

    def test_decrease_quantity_reflects_in_item_total_and_subtotal(self):
        """Verify that after increasing to 3 and clicking minus, item total and subtotal reflect correctly."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        unit_price = self.cart_page.get_cart_item_unit_price()
        self.cart_page.click_plus_button(self.minimum_quantity_product)
        self.cart_page.click_plus_button(self.minimum_quantity_product)
        self.cart_page.click_minus_button(self.minimum_quantity_product)
        quantity   = self.cart_page.get_cart_item_quantity()
        self._validate_item_total_and_subtotal(unit_price, quantity)

    # =====================================================
    # Negative Test Cases
    # Validates invalid add to cart scenarios
    # =====================================================

    def test_add_out_of_stock_product_to_cart(self):
        """Verify add to cart button is disabled for out of stock product."""
        self.search_page.click_search()
        self.search_page.search_for_product(self.out_of_stock_product)
        is_out_of_stock = self.cart_page.is_product_sold_out(self.out_of_stock_product)
        if is_out_of_stock:
            self.search_page.click_product_link(self.out_of_stock_product)
            assert self.cart_page.is_sold_out_button_disabled(), (
                f"Expected 'Sold Out' button to be disabled for "
                f"'{self.out_of_stock_product}' but it was enabled."
            )

    def test_buy_now_disabled_for_out_of_stock_product(self):
        """Verify clicking Buy Now on a sold out product does not navigate away."""
        self.search_page.click_search()
        self.search_page.search_for_product(self.out_of_stock_product)
        is_out_of_stock = self.cart_page.is_product_sold_out(self.out_of_stock_product)
        if is_out_of_stock:
            self.search_page.click_product_link(self.out_of_stock_product)
            self.cart_page.verify_buy_now_does_not_navigate(self.out_of_stock_product)

    def test_minus_button_disabled_at_minimum_quantity(self):
        """Verify minus button is disabled when product quantity is 1 in cart."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        assert self.cart_page.is_minus_button_disabled(self.minimum_quantity_product), (
            f"Expected minus button to be disabled at quantity 1 "
            f"for '{self.minimum_quantity_product}' but it was enabled."
        )

    # =====================================================
    # Edge Case Test Cases
    # Validates boundary and abnormal cart scenarios
    # =====================================================

    def test_cart_badge_updates_after_adding_product(self):
        """Verify cart badge count increments correctly after adding product."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        self.cart_page.wait_for_badge_count(1)
        assert self.cart_page.get_cart_badge_count() == 1, (
            f"Expected cart badge to show '1' after first add "
            f"but got '{self.cart_page.get_cart_badge_count()}'."
        )
        self.cart_page.click_plus_button(self.minimum_quantity_product)
        self.cart_page.wait_for_badge_count(2)
        assert self.cart_page.get_cart_badge_count() == 2, (
            f"Expected cart badge to show '2' after increasing quantity "
            f"but got '{self.cart_page.get_cart_badge_count()}'."
        )

    def test_cart_persists_after_page_refresh(self):
        """Verify cart contents persist after page refresh."""
        self._search_and_add_to_cart(self.minimum_quantity_product)
        count_before_refresh = self.cart_page.get_cart_badge_count()
        self.cart_page.refresh_page()
        count_after_refresh  = self.cart_page.get_cart_badge_count()
        assert count_before_refresh == count_after_refresh, (
            f"Expected cart badge '{count_before_refresh}' to persist after refresh "
            f"but got '{count_after_refresh}'."
        )