from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AddToCart:
    """
    Page Object для работы с корзиной товаров.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация работы с корзиной.

        :param driver: WebDriver - Экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Локаторы
        self.buy_button = (
            By.XPATH,
            "(//button[contains(@class, 'product-buttons__main-action')])[1]"
        )
        self.cart_icon = (By.XPATH, "//button[@aria-label='Корзина']")
        self.cart_counter = (
            By.CSS_SELECTOR,
            ".header-controls__btn .chg-indicator"
        )
        self.delete_button = (
            By.CSS_SELECTOR,
            "button.cart-item__delete-button"
        )

    def add_product_to_cart(self) -> None:
        """
        Добавить товар в корзину.
        :return: None
        """
        self.driver.execute_script("window.scrollTo(0, 300);")
        element = self.wait.until(
            EC.element_to_be_clickable(self.buy_button)
        )
        self.driver.execute_script("arguments[0].click();", element)

        self.wait.until(
            lambda driver: driver.find_element(
                *self.cart_counter).text.strip() != ""
        )

    def open_cart(self) -> None:
        """
        Открыть корзину товаров.
        :return: None
        """
        to_cart = self.driver.find_element(*self.cart_icon)
        to_cart.click()

    def delete_from_cart(self) -> None:
        """
        Удалить товар из корзины.
        :return: None
        """
        delete_btn = self.wait.until(
            EC.element_to_be_clickable(self.delete_button)
        )
        delete_btn.click()
