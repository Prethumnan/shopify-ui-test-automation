from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from utils.selenium_utils import SeleniumUtils


class AddToCartPage:

    # =====================================================
    # Locators — Product Page
    # =====================================================

    _ADD_TO_CART_BUTTON   = (By.XPATH, "//button[@name='add' and contains(@class,'product-form__submit')]")
    _BUY_NOW_BUTTON       = (By.XPATH, "//button[normalize-space(text())='Buy it now']")
    _SOLD_OUT_BTN         = (By.XPATH, "//button[contains(@id,'ProductSubmitButton')]")
    _SOLD_OUT_BADGE_XPATH = (By.XPATH, "//span[normalize-space(text())='Sold out']")
    _SOLD_OUT_PRICE_XPATH = (By.XPATH, "//div[contains(@class,'price--sold-out')]")

    # =====================================================
    # Locators — Cart Drawer
    # =====================================================

    _CART_ICON              = (By.XPATH, "//a[@href='/cart']")
    _EMPTY_CART_MSG         = (By.XPATH, "//p[contains(text(),'Your cart is empty')]")
    _CART_BADGE_XPATH       = (By.XPATH, "//div[contains(@class,'cart-count-bubble')]//span[@aria-hidden='true']")
    _CART_SUBTOTAL_XPATH    = (By.XPATH, "//p[contains(@class,'totals__subtotal-value')]")
    _CART_ITEM_TOTAL_XPATH  = (By.XPATH, "//div[contains(@class,'cart-item__price-wrapper')]//span[contains(@class,'price--end')]")
    _CART_ITEM_PRICE_XPATH  = (By.XPATH, "//div[contains(@class,'product-option') and contains(text(),'$')]")
    _QUANTITY_INPUT_XPATH   = (By.XPATH, "//input[contains(@class,'quantity__input')]")

    # =====================================================
    # Locators — Quantity Buttons (dynamic — string templates)
    # =====================================================

    _MINUS_BUTTON_XPATH     = "//button[@name='minus']"
    _PLUS_BUTTON_XPATH      = "//button[@name='plus']"
    _REMOVE_BUTTON_XPATH    = "//a[@aria-label='Remove {} from your shopping cart']"

    # =====================================================
    # CSS Classes
    # =====================================================

    _MINUS_BUTTON_CSS_CLASS = "disabled"

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self, driver):
        self.driver     = driver
        self.sele_utils = SeleniumUtils(self.driver)

    # =====================================================
    # Locator Builder Methods
    # =====================================================

    def get_minus_button_locator(self, product_name: str) -> tuple:
        """
        Returns the minus button locator for the cart.

        Args:
            product_name: Reserved for future multi-product support.

        Returns:
            Tuple locator for the minus button.
        """
        return (By.XPATH, self._MINUS_BUTTON_XPATH)

    def get_plus_button_locator(self, product_name: str) -> tuple:
        """
        Returns the plus button locator for the cart.

        Args:
            product_name: Reserved for future multi-product support.

        Returns:
            Tuple locator for the plus button.
        """
        return (By.XPATH, self._PLUS_BUTTON_XPATH)

    def get_remove_button_locator(self, product_name: str) -> tuple:
        """
        Builds the remove button locator for a given product name.

        Args:
            product_name: The product name to build the locator for.

        Returns:
            Tuple locator for the remove button.
        """
        return (By.XPATH, self._REMOVE_BUTTON_XPATH.format(product_name))

    # =====================================================
    # Product Page Actions
    # =====================================================

    def click_add_to_cart(self) -> None:
        """Clicks the Add to Cart button on the product page."""
        self.sele_utils.click(self._ADD_TO_CART_BUTTON)

    def click_buy_now_button(self) -> None:
        """
        Attempts to click the Buy Now button using JavaScript.
        js_click is used to force click even if the button is disabled.
        """
        self.sele_utils.js_click(self._BUY_NOW_BUTTON)

    # =====================================================
    # Cart Drawer Actions
    # =====================================================

    def navigate_to_cart(self) -> None:
        """Navigates to the cart page by clicking the cart icon."""
        self.sele_utils.click(self._CART_ICON)

    def click_plus_button(self, product_name: str) -> None:
        """
        Scrolls to and clicks the plus quantity button in the cart.

        Args:
            product_name: The product name to increase quantity for.
        """
        locator = self.get_plus_button_locator(product_name)
        self.sele_utils.scroll_into_view(locator)
        self.sele_utils.click(locator)

    def click_minus_button(self, product_name: str) -> None:
        """
        Scrolls to and clicks the minus quantity button in the cart.

        Args:
            product_name: The product name to decrease quantity for.
        """
        locator = self.get_minus_button_locator(product_name)
        self.sele_utils.scroll_into_view(locator)
        self.sele_utils.click(locator)

    def remove_product_from_cart(self, product_name: str) -> None:
        """
        Clicks the remove button for a specific product in the cart.

        Args:
            product_name: The product name to remove.
        """
        self.sele_utils.click(self.get_remove_button_locator(product_name))

    def refresh_page(self) -> None:
        """Refreshes the current page to verify cart persistence."""
        self.sele_utils.driver.refresh()

    # =====================================================
    # Cart Data Retrieval
    # =====================================================

    def get_cart_item_total(self, expected_min_value: float = None) -> float:
        """
        Waits until the cart item total updates and returns the new value.
        Uses an explicit lambda wait to handle DOM refresh after quantity change.

        Args:
            expected_min_value: If provided, waits until total exceeds this value
                                to confirm the DOM has updated after a quantity change.

        Returns:
            Float value of the updated cart item total.
        """
        def total_has_updated(driver):
            element = driver.find_element(*self._CART_ITEM_TOTAL_XPATH)
            text    = element.text.strip()
            value   = self._parse_price(text) if text else 0
            if expected_min_value is not None:
                return value if value > expected_min_value else False
            return value if value > 0 else False

        return WebDriverWait(self.sele_utils.driver, 30).until(total_has_updated)

    def get_cart_subtotal(self) -> float:
        """
        Returns the subtotal shown at the bottom of the cart drawer.

        Returns:
            Float value of the cart subtotal.
        """
        text = self.sele_utils.get_text(self._CART_SUBTOTAL_XPATH)
        return self._parse_price(text)

    def get_cart_item_unit_price(self) -> float:
        """
        Returns the unit price of the cart item.

        Returns:
            Float value of the unit price.
        """
        text = self.sele_utils.get_text(self._CART_ITEM_PRICE_XPATH)
        return self._parse_price(text)

    def get_cart_item_quantity(self) -> int:
        """
        Returns the current quantity shown in the quantity input field.

        Returns:
            Integer value of the current quantity.
        """
        element = self.sele_utils.wait_until_visible(self._QUANTITY_INPUT_XPATH)
        return int(element.get_attribute("value"))

    def get_cart_badge_count(self) -> int:
        """
        Returns the current cart badge count shown on the cart icon in the header.

        Returns:
            Integer value of the cart badge count.
        """
        text = self.sele_utils.get_text(self._CART_BADGE_XPATH)
        return int(text.strip())

    # =====================================================
    # Validation Methods
    # =====================================================

    def is_product_sold_out(self, product_name: str) -> bool:
        """
        Validates that the product displayed in search results is marked as sold out.
        Scrolls to the sold out badge before checking visibility.

        Args:
            product_name: The product name to verify sold out status for.

        Returns:
            True if product is marked as sold out, False otherwise.
        """
        self.sele_utils.scroll_into_view(self._SOLD_OUT_BADGE_XPATH)
        return (
            self.sele_utils.is_displayed(self._SOLD_OUT_BADGE_XPATH) and
            self.sele_utils.is_displayed(self._SOLD_OUT_PRICE_XPATH)
        )

    def is_sold_out_button_disabled(self) -> bool:
        """
        Checks whether the Sold Out button on the product page is disabled.

        Returns:
            True if the button is disabled, False otherwise.
        """
        return self.sele_utils.is_element_disabled(self._SOLD_OUT_BTN)

    def is_minus_button_disabled(self, product_name: str) -> bool:
        """
        Checks whether the minus button has the disabled CSS class at quantity 1.
        Retries on StaleElementReferenceException since the cart DOM refreshes frequently.

        Args:
            product_name: The product name to check the minus button for.

        Returns:
            True if minus button is disabled, False otherwise.
        """
        MAX_RETRIES = 3
        locator     = self.get_minus_button_locator(product_name)

        for attempt in range(MAX_RETRIES):
            try:
                self.sele_utils.scroll_into_view(locator)
                return self.sele_utils.has_class(locator, self._MINUS_BUTTON_CSS_CLASS)
            except StaleElementReferenceException:
                if attempt == MAX_RETRIES - 1:
                    raise

    def is_cart_empty(self) -> bool:
        """
        Checks whether the cart is empty by verifying the empty cart message is displayed.

        Returns:
            True if cart is empty, False otherwise.
        """
        return self.sele_utils.is_displayed(self._EMPTY_CART_MSG)

    def wait_for_badge_count(self, expected_count: int) -> None:
        """
        Waits until the cart badge count matches the expected value.
        Used to ensure the DOM has updated before reading the badge count.

        Args:
            expected_count: The expected badge count to wait for.
        """
        self.sele_utils.wait_until_text_equals(
            self._CART_BADGE_XPATH, str(expected_count)
        )

    def verify_buy_now_does_not_navigate(self, product_name: str) -> None:
        """
        Verifies that clicking Buy Now on a sold out product does not navigate away from the page.
        Captures URL before and after the click and asserts they are equal.

        Args:
            product_name: The out of stock product name to verify against.
        """
        url_before_click = self.sele_utils.get_current_url()
        self.click_buy_now_button()
        url_after_click  = self.sele_utils.get_current_url()
        assert url_before_click == url_after_click, (
            f"Expected page to stay on '{url_before_click}' after clicking Buy Now "
            f"for product '{product_name}' but navigated to '{url_after_click}'."
        )

    # =====================================================
    # Private Helper Methods
    # =====================================================

    def _parse_price(self, price_text: str) -> float:
        """
        Parses a price string from the UI into a float value.
        Handles formats like '$749.95', '$1,499.90', '$1,499.90 USD'.

        Args:
            price_text: Raw price string from the UI.

        Returns:
            Float value of the price.
        """
        return float(
            price_text.replace("$", "")
                      .replace(",", "")
                      .replace("USD", "")
                      .strip()
        )

