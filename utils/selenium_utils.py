from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class SeleniumUtils:

    # =====================================================
    # Constants
    # =====================================================

    _DEFAULT_TIMEOUT = 30
    _MAX_RETRIES     = 3

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, self._DEFAULT_TIMEOUT)

    # =====================================================
    # Wait Methods
    # =====================================================

    def wait_until_visible(self, locator):
        """
        Waits until the element is visible on the page.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            WebElement once visible.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_all_visible(self, locator):
        """
        Waits until all elements matching the locator are visible.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            List of visible WebElements.
        """
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_until_clickable(self, locator):
        """
        Waits until the element is clickable.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            WebElement once clickable.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_present(self, locator):
        """
        Waits until the element is present in the DOM.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            WebElement once present.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_invisible(self, locator):
        """
        Waits until the element is no longer visible.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            True once element is invisible.
        """
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_until_text_equals(self, locator, expected_text: str) -> str:
        """
        Waits until the element's text equals the expected value.
        Used to confirm DOM has updated after dynamic UI changes.

        Args:
            locator:       Tuple locator (By.XPATH, '...').
            expected_text: The text value to wait for.

        Returns:
            The element text once it matches.
        """
        def text_matches(driver):
            element = driver.find_element(*locator)
            return element.text.strip() if element.text.strip() == expected_text else False

        return self.wait.until(text_matches)

    # =====================================================
    # Basic Actions
    # =====================================================

    def click(self, locator) -> None:
        """
        Waits for the element to be clickable and clicks it.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_clickable(locator)
        element.click()

    def send_keys(self, locator, text: str) -> None:
        """
        Clears the input field and types the given text.

        Args:
            locator: Tuple locator (By.XPATH, '...').
            text:    Text to type into the field.
        """
        element = self.wait_until_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, element_or_locator) -> str:
        """
        Returns the visible text of an element.
        Accepts either a locator tuple or a WebElement directly.

        Args:
            element_or_locator: Tuple locator (By.XPATH, '...') or WebElement.

        Returns:
            Visible text of the element.
        """
        if isinstance(element_or_locator, tuple):
            element = self.wait_until_visible(element_or_locator)
        else:
            element = element_or_locator
        return element.text

    def find_elements(self, locator) -> list:
        """
        Waits for at least one element to be present then returns all matches.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            List of WebElements.
        """
        self.wait_until_present(locator)
        return self.driver.find_elements(*locator)

    def is_displayed(self, locator) -> bool:
        """
        Checks whether an element is visible on the page.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            True if element is visible, False if timeout occurs.
        """
        try:
            return self.wait_until_visible(locator).is_displayed()
        except TimeoutException:
            return False

    def is_element_disabled(self, locator) -> bool:
        """
        Checks whether an element is disabled via the HTML disabled attribute.

        Args:
            locator: Tuple locator (By.XPATH, '...').

        Returns:
            True if element is disabled, False otherwise.
        """
        try:
            element = self.wait_until_present(locator)
            return not element.is_enabled()
        except TimeoutException:
            return False

    def has_class(self, locator, class_name: str) -> bool:
        """
        Checks whether an element contains a specific CSS class.
        Use this when disabled state is indicated by a CSS class, not the HTML disabled attribute.

        Args:
            locator:    Tuple locator (By.XPATH, '...').
            class_name: CSS class name to check for.

        Returns:
            True if element has the class, False otherwise.
        """
        element = self.wait_until_present(locator)
        classes = element.get_attribute("class")
        return class_name in classes.split()

    def get_current_url(self) -> str:
        """
        Returns the current page URL.

        Returns:
            Current URL string.
        """
        return self.driver.current_url

    # =====================================================
    # Keyboard Actions
    # =====================================================

    def press_enter(self, locator) -> None:
        """
        Sends the ENTER key to the element.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_visible(locator)
        element.send_keys(Keys.ENTER)

    def press_tab(self, locator) -> None:
        """
        Sends the TAB key to the element.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_visible(locator)
        element.send_keys(Keys.TAB)

    # =====================================================
    # Mouse Actions
    # =====================================================

    def hover(self, locator) -> None:
        """
        Hovers over an element using ActionChains.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def double_click(self, locator) -> None:
        """
        Double-clicks an element.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_clickable(locator)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator) -> None:
        """
        Right-clicks an element.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_clickable(locator)
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop(self, source_locator, target_locator) -> None:
        """
        Drags an element from source to target.

        Args:
            source_locator: Tuple locator for the element to drag.
            target_locator: Tuple locator for the drop target.
        """
        source = self.wait_until_visible(source_locator)
        target = self.wait_until_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def move_to_element(self, element_or_locator) -> None:
        """
        Moves the mouse cursor to an element.
        Accepts either a locator tuple or a WebElement directly.

        Args:
            element_or_locator: Tuple locator (By.XPATH, '...') or WebElement.
        """
        if isinstance(element_or_locator, tuple):
            element = self.wait_until_visible(element_or_locator)
        else:
            element = element_or_locator
        ActionChains(self.driver).move_to_element(element).perform()

    # =====================================================
    # Scroll Methods
    # =====================================================

    def scroll_into_view(self, locator) -> None:
        """
        Scrolls a locator-based element into view using JavaScript.
        Retries on StaleElementReferenceException since the DOM may refresh mid-scroll.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        for attempt in range(self._MAX_RETRIES):
            try:
                element = self.wait_until_present(locator)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
                    element
                )
                return
            except StaleElementReferenceException:
                if attempt == self._MAX_RETRIES - 1:
                    raise

    def scroll_into_view_element(self, element_or_locator) -> None:
        """
        Scrolls an element into view using JavaScript.
        Accepts either a WebElement or a tuple locator.
        Use this when iterating over a list of already-fetched WebElements.

        Args:
            element_or_locator: WebElement or tuple locator (By.XPATH, '...').
        """
        if isinstance(element_or_locator, tuple):
            element = self.wait_until_present(element_or_locator)
        else:
            element = element_or_locator
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            element
        )

    def scroll_to_bottom(self) -> None:
        """Scrolls the page to the very bottom."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self) -> None:
        """Scrolls the page to the very top."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    # =====================================================
    # JavaScript Methods
    # =====================================================

    def js_click(self, locator) -> None:
        """
        Clicks an element using JavaScript.
        Use when standard click fails due to element not being interactable.

        Args:
            locator: Tuple locator (By.XPATH, '...').
        """
        element = self.wait_until_present(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # =====================================================
    # Dropdown Methods
    # =====================================================

    def select_by_visible_text(self, locator, text: str) -> None:
        """
        Selects a dropdown option by its visible text.

        Args:
            locator: Tuple locator (By.XPATH, '...').
            text:    Visible text of the option to select.
        """
        dropdown = Select(self.wait_until_visible(locator))
        dropdown.select_by_visible_text(text)

    def select_by_value(self, locator, value: str) -> None:
        """
        Selects a dropdown option by its value attribute.

        Args:
            locator: Tuple locator (By.XPATH, '...').
            value:   Value attribute of the option to select.
        """
        dropdown = Select(self.wait_until_visible(locator))
        dropdown.select_by_value(value)

    # =====================================================
    # Alert Handling
    # =====================================================

    def accept_alert(self) -> None:
        """Waits for an alert to appear and accepts it."""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self) -> None:
        """Waits for an alert to appear and dismisses it."""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self) -> str:
        """
        Waits for an alert and returns its text.

        Returns:
            Alert message text.
        """
        self.wait.until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    # =====================================================
    # Frame Handling
    # =====================================================

    def switch_to_frame(self, locator) -> None:
        """
        Switches WebDriver context into an iframe.

        Args:
            locator: Tuple locator (By.XPATH, '...') of the iframe element.
        """
        frame = self.wait_until_present(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self) -> None:
        """Switches WebDriver context back to the main document."""
        self.driver.switch_to.default_content()

    # =====================================================
    # Window Handling
    # =====================================================

    def switch_to_new_window(self) -> None:
        """Switches WebDriver context to the most recently opened window or tab."""
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    # =====================================================
    # Screenshot
    # =====================================================

    def take_screenshot(self, file_name: str) -> None:
        """
        Saves a screenshot to the given file path.

        Args:
            file_name: Full file path including filename and extension.
        """
        self.driver.save_screenshot(file_name)