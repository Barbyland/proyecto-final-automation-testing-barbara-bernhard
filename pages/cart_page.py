from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def wait_until_loaded(self):
        self.wait_for_url_contains("/cart.html")
        self.wait_for_visible(self.CART_LIST)

    def get_item_names(self):
        return [
            item.find_element(*self.ITEM_NAME).text
            for item in self.find_all(self.CART_ITEM)
        ]

    def get_items_count(self):
        return len(self.find_all(self.CART_ITEM))

    def start_checkout(self):
        self.click_with_javascript(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("/checkout-step-one.html")
