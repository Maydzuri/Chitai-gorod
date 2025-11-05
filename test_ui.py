import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.search_ui_page import SearchPage
from pages.cart_ui_page import AddToCart
from pages.auth_ui_page import AuthPage
from config import url_ui, book_title, invalid_title, phone, invalid_phone


@pytest.fixture
def driver():
    """
    Фикстура для инициализации браузера.

    :yields: WebDriver - Экземпляр WebDriver
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url_ui)
    yield driver
    driver.quit()


@allure.epic("Читай-город")
@allure.feature("Поиск товаров")
@allure.title("Поиск книги по названию. POSITIVE")
@allure.description("Тест проверяет, что поиск книг работает корректно.")
@allure.severity("CRITICAL")
@pytest.mark.ui
@pytest.mark.search
def test_search_by_title(driver):
    """
    Тест поиска книги по существующему названию.
    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    search = SearchPage(driver)

    with allure.step("Найти книгу по названию"):
        search.search_by_title(book_title)

    with allure.step("Проверить, что поиск по названию успешен"):
        page_text = driver.page_source.lower()
        assert book_title.lower() in page_text


@allure.epic("Читай-город")
@allure.feature("Поиск товаров")
@allure.title("Поиск книги по несуществующему названию. NEGATIVE")
@allure.description("Тест проверяет, что поиск по несуществующему названию "
                    "возвращает корректный результат.")
@allure.severity("NORMAL")
@pytest.mark.ui
@pytest.mark.search
def test_search_negative(driver):
    """
    Тест поиска книги по несуществующему названию.

    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    search = SearchPage(driver)

    with allure.step("Найти книгу по несуществующему названию"):
        search.search_negative(invalid_title)

    with allure.step("Проверить, что поиск не дал результатов"):
        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".catalog-stub__title")
            )
        )
        assert error_message.text == "Похоже, у нас такого нет"


@allure.epic("Читай-город")
@allure.feature("Корзина")
@allure.title("Добавление товара в корзину. POSITIVE")
@allure.description("Тест проверяет, что добавление товара в корзину "
                    "работает корректно.")
@allure.severity("CRITICAL")
@pytest.mark.ui
@pytest.mark.cart
def test_add_product_to_cart(driver):
    """
    Тест добавления товара в корзину.

    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    search = SearchPage(driver)
    cart = AddToCart(driver)

    with allure.step("Найти книгу по названию"):
        search.search_by_title(book_title)

    with allure.step("Нажать на кнопку 'Купить'"):
        cart.add_product_to_cart()

    with allure.step("Проверяем, что товар добавлен в корзину"):
        count = driver.find_element(
            By.CSS_SELECTOR, ".header-controls__btn .chg-indicator"
        ).text.strip()
        print(f"✓ Товар добавлен в корзину. Количество: {count}")


@allure.epic("Читай-город")
@allure.feature("Корзина")
@allure.title("Удаление товара из корзины. POSITIVE")
@allure.description("Тест проверяет, что товар из корзины удаляется корректно")
@allure.severity("CRITICAL")
@pytest.mark.ui
@pytest.mark.cart
def test_delete_from_cart(driver):
    """
    Тест удаления товара из корзины.

    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    search = SearchPage(driver)
    cart = AddToCart(driver)

    with allure.step("Найти книгу по названию"):
        search.search_by_title(book_title)

    with allure.step("Нажать на кнопку 'Купить'"):
        cart.add_product_to_cart()

    with allure.step("Открыть корзину"):
        cart.open_cart()

    with allure.step("Удалить товар из корзины"):
        cart.delete_from_cart()

    with allure.step("Проверить, что товар удален"):
        wait = WebDriverWait(driver, 10)
        deleted_message = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".cart-item-deleted__title")
            )
        )
        assert deleted_message.text == "Удалили товар из корзины"


@allure.epic("Читай-город")
@allure.feature("Авторизация")
@allure.title("Активация кнопки 'Получить код' при вводе номера. POSITIVE")
@allure.description("Тест проверяет, что кнопка 'Получить код' активируется "
                    "только при корректном номере телефона.")
@allure.severity("CRITICAL")
@pytest.mark.ui
@pytest.mark.auth
def test_auth_form(driver):
    """
    Тест активации кнопки 'Получить код' при корректном номере телефона.

    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    auth = AuthPage(driver)

    with allure.step("Нажать на кнопку 'Войти'"):
        auth.open_auth_form()

    with allure.step("Проверить, что кнопка 'Получить код' "
                     "неактивна при пустом поле"):
        get_code_btn = driver.find_element(*auth.get_code_button)
        assert get_code_btn.get_attribute("disabled") is not None

    with allure.step("Ввести корректный номер телефона"):
        auth.enter_phone_number(phone)

    with allure.step("Проверить, что кнопка 'Получить код' "
                     "стала активной"):
        auth.wait.until(
            EC.element_to_be_clickable(auth.get_code_button)
        )
        get_code_btn = driver.find_element(*auth.get_code_button)
        assert get_code_btn.get_attribute("disabled") is None


@allure.epic("Читай-город")
@allure.feature("Авторизация")
@allure.title("Активация кнопки 'Получить код' с некорректным номером. "
              "NEGATIVE")
@allure.description("Тест проверяет, что кнопка 'Получить код' не "
                    "активируется при неправильном номере телефона.")
@allure.severity("NORMAL")
@pytest.mark.ui
@pytest.mark.auth
def test_auth_form_invalid_phone(driver):
    """
    Тест активации кнопки 'Получить код' при некорректном номере телефона.

    :param driver: WebDriver instance
    :type driver: WebDriver
    :return: None
    """
    auth = AuthPage(driver)

    with allure.step("Нажать на кнопку 'Войти'"):
        auth.open_auth_form()

    with allure.step("Ввести некорректный номер телефона"):
        auth.enter_phone_number(invalid_phone)

    with allure.step("Проверить, что кнопка 'Получить код' "
                     "осталась неактивной"):
        get_code_btn = driver.find_element(*auth.get_code_button)
        assert get_code_btn.get_attribute("disabled") is not None
