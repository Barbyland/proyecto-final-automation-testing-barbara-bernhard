from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    BRAND = (By.CLASS_NAME, "app_logo")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    PRODUCT = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def wait_until_loaded(self):
        self.wait_for_url_contains("/inventory.html")
        self.wait_for_visible(self.PRODUCT)

    def get_title(self):
        return self.wait_for_visible(self.TITLE).text

    def get_brand(self):
        return self.wait_for_visible(self.BRAND).text

    def has_menu_button(self):
        return self.wait_for_visible(self.MENU_BUTTON).is_displayed()

    def has_sort_select(self):
        return self.wait_for_visible(self.SORT_SELECT).is_displayed()

    def get_products(self):
        self.wait_for_visible(self.PRODUCT)
        return self.find_all(self.PRODUCT)

    def get_first_product_name_and_price(self):
        first_product = self.get_products()[0]
        name = first_product.find_element(*self.PRODUCT_NAME).text
        price = first_product.find_element(*self.PRODUCT_PRICE).text
        return name, price

    def add_first_product_to_cart(self):
        first_product = self.get_products()[0]
        name = first_product.find_element(*self.PRODUCT_NAME).text
        add_button = first_product.find_element(*self.ADD_TO_CART_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
        self.driver.execute_script("arguments[0].click();", add_button)
        self.wait_for_visible(self.CART_BADGE)
        return name

    def remove_first_product_from_cart(self):
        self.click_with_javascript(self.REMOVE_BUTTON)
        self.wait_for_invisible(self.CART_BADGE)

    def get_cart_count(self):
        return self.wait_for_visible(self.CART_BADGE).text

    def open_cart(self):
        self.click_with_javascript(self.CART_LINK)
        self.wait_for_url_contains("/cart.html")
