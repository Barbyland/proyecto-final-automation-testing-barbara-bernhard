import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_json
from utils.logger import get_logger


test_data = load_json("ui_users.json")
logger = get_logger("ui")


def login_with_valid_user(driver):
    user = test_data["valid_user"]
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.open()
    login_page.login(user["username"], user["password"])
    inventory_page.wait_until_loaded()
    return inventory_page


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
def test_login_exitoso_redirige_al_inventario(driver):
    logger.info("Validando login exitoso")
    inventory_page = login_with_valid_user(driver)

    assert "/inventory.html" in driver.current_url
    assert inventory_page.get_title() == "Products"
    assert inventory_page.get_brand() == "Swag Labs"


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize(
    "invalid_user",
    test_data["invalid_users"],
    ids=[user["case"] for user in test_data["invalid_users"]],
)
def test_login_invalido_muestra_mensaje_de_error(driver, invalid_user):
    logger.info("Validando login invalido: %s", invalid_user["case"])
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login(invalid_user["username"], invalid_user["password"])

    assert invalid_user["expected_error"] in login_page.get_error_message()


@pytest.mark.ui
@pytest.mark.catalog
@pytest.mark.regression
def test_catalogo_muestra_productos_y_elementos_principales(driver):
    logger.info("Validando catalogo de productos")
    inventory_page = login_with_valid_user(driver)
    product_name, product_price = inventory_page.get_first_product_name_and_price()

    assert len(inventory_page.get_products()) > 0
    assert product_name != ""
    assert product_price.startswith("$")
    assert inventory_page.has_menu_button()
    assert inventory_page.has_sort_select()


@pytest.mark.ui
@pytest.mark.cart
@pytest.mark.smoke
def test_agregar_primer_producto_al_carrito(driver):
    logger.info("Validando agregado de producto al carrito")
    inventory_page = login_with_valid_user(driver)

    product_name = inventory_page.add_first_product_to_cart()
    assert inventory_page.get_cart_count() == "1"

    inventory_page.open_cart()
    cart_page = CartPage(driver)
    cart_page.wait_until_loaded()

    assert cart_page.get_items_count() == 1
    assert product_name in cart_page.get_item_names()


@pytest.mark.ui
@pytest.mark.cart
@pytest.mark.regression
def test_remover_producto_del_carrito_actualiza_contador(driver):
    logger.info("Validando remocion de producto")
    inventory_page = login_with_valid_user(driver)

    inventory_page.add_first_product_to_cart()
    assert inventory_page.get_cart_count() == "1"

    inventory_page.remove_first_product_from_cart()

    assert len(driver.find_elements(*InventoryPage.CART_BADGE)) == 0


@pytest.mark.ui
@pytest.mark.checkout
@pytest.mark.regression
def test_checkout_completo_finaliza_compra(driver):
    logger.info("Validando flujo completo de checkout")
    inventory_page = login_with_valid_user(driver)
    checkout_user = test_data["checkout_user"]

    product_name = inventory_page.add_first_product_to_cart()
    inventory_page.open_cart()

    cart_page = CartPage(driver)
    cart_page.wait_until_loaded()
    assert product_name in cart_page.get_item_names()

    cart_page.start_checkout()
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_information(
        checkout_user["first_name"],
        checkout_user["last_name"],
        checkout_user["postal_code"],
    )

    assert checkout_page.get_summary_total().startswith("Total: $")

    checkout_page.finish_purchase()
    assert checkout_page.get_complete_message() == "Thank you for your order!"
