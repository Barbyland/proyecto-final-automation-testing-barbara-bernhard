from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def fill_information(self, first_name, last_name, postal_code):
        self.wait_for_url_contains("/checkout-step-one.html")
        self.set_input_value(self.FIRST_NAME_INPUT, first_name)
        self.set_input_value(self.LAST_NAME_INPUT, last_name)
        self.set_input_value(self.POSTAL_CODE_INPUT, postal_code)
        self.click_with_javascript(self.CONTINUE_BUTTON)
        self.wait_for_url_contains("/checkout-step-two.html")

    def get_summary_total(self):
        self.wait_for_url_contains("/checkout-step-two.html")
        return self.wait_for_visible(self.SUMMARY_TOTAL).text

    def finish_purchase(self):
        self.click_with_javascript(self.FINISH_BUTTON)
        self.wait_for_url_contains("/checkout-complete.html")

    def get_complete_message(self):
        self.wait_for_url_contains("/checkout-complete.html")
        return self.wait_for_visible(self.COMPLETE_HEADER).text
