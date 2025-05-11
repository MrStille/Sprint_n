from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 5

    def __init__(self, driver):
        self.driver = driver

    def wait_element_visible(self, locator):
        return WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(EC.visibility_of_element_located(locator))

    def wait_element_visible_custom_duration(self, locator, seconds):
        return WebDriverWait(self.driver, seconds).until(EC.visibility_of_element_located(locator))

    def wait_element_not_visible(self, locator):
        return WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(EC.invisibility_of_element_located(locator))

    def wait_element_has_text(self, locator, text):
        return WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
            EC.text_to_be_present_in_element(locator, str(text)))

    def wait_util_element_text_changes(self, locator, text):
        return WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
            lambda drv: drv.find_element(*locator).text != str(text))

    def format_locator(self, locator, text):
        new_locator = (locator[0], locator[1].format(text))
        return new_locator