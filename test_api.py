import pytest
import allure
from pages.api_client import CartAPI
from config import product_id


@pytest.fixture
def api_client() -> CartAPI:
    """
    Фикстура для создания API клиента.

    :return: CartAPI instance
    :rtype: CartAPI
    """
    return CartAPI()


@allure.epic("Читай-город API")
@allure.feature("Корзина")
@allure.title("Добавление товара в корзину. POSITIVE")
@allure.description("Тест проверяет добавление товара в корзину через API.")
@allure.severity("CRITICAL")
@pytest.mark.api
@pytest.mark.cart
def test_add_product_to_cart(api_client: CartAPI) -> None:
    """
    Тест добавления товара в корзину.

    :param api_client: API клиент
    :type api_client: CartAPI
    :return: None
    """
    with allure.step("Добавить товар в корзину"):
        result = api_client.add_product_to_cart(product_id)

    with allure.step("Проверить успешный ответ"):
        assert result.status_code == 200


@allure.epic("Читай-город API")
@allure.feature("Корзина")
@allure.title("Просмотр корзины. POSITIVE")
@allure.description("Тест проверяет получение содержимого корзины.")
@allure.severity("NORMAL")
@pytest.mark.api
@pytest.mark.cart
def test_get_cart(api_client: CartAPI) -> None:
    """
    Тест получения содержимого корзины.

    :param api_client: API клиент
    :type api_client: CartAPI
    :return: None
    """
    with allure.step("Добавить товар в корзину"):
        result = api_client.add_product_to_cart(product_id)

    with allure.step("Получить корзину"):
        result = api_client.get_cart()

    with allure.step("Проверить успешный ответ"):
        assert result.status_code == 200


@allure.epic("Читай-город API")
@allure.feature("Корзина")
@allure.title("Удаление товара из корзины. POSITIVE")
@allure.description("Тест проверяет удаление товара из корзины.")
@allure.severity("CRITICAL")
@pytest.mark.api
@pytest.mark.cart
def test_remove_product_from_cart(api_client: CartAPI) -> None:
    """
    Тест удаления товара из корзины.

    :param api_client: API клиент
    :type api_client: CartAPI
    :return: None
    """
    with allure.step("Добавить товар в корзину"):
        add_result = api_client.add_product_to_cart(product_id)
        assert add_result.status_code == 200

    with allure.step("Получить корзину и найти cart_product_id"):
        cart_result = api_client.get_cart()
        assert cart_result.status_code == 200

        cart_data = cart_result.json()
        assert len(cart_data["products"]) > 0

        # Находим cart_product_id (поле "id" в products)
        cart_product_id = cart_data["products"][0]["id"]

    with allure.step("Удалить товар из корзины"):
        result = api_client.remove_from_cart(cart_product_id)

    with allure.step("Проверить успешное удаление"):
        assert result.status_code == 204

    with allure.step("Проверить что корзина пуста"):
        cart_result = api_client.get_cart()
        assert cart_result.status_code == 200
        cart_data = cart_result.json()
        assert len(cart_data["products"]) == 0


@allure.epic("Читай-город API")
@allure.feature("Корзина")
@allure.title("Добавление товара без ID в корзину. NEGATIVE")
@allure.description("Тест проверяет ошибку при добавлении товара без ID")
@allure.severity("NORMAL")
@pytest.mark.api
@pytest.mark.negative
def test_add_product_without_id(api_client: CartAPI) -> None:
    """
    Негативный тест: добавление товара без ID.

    :param api_client: API клиент
    :type api_client: CartAPI
    :return: None
    """
    with allure.step("Отправить POST запрос без id товара"):
        result = api_client.add_product_without_id()

    with allure.step("Проверить что вернулась ошибка 400"):
        assert result.status_code == 400


@allure.epic("Читай-город API")
@allure.feature("Корзина")
@allure.title("Просмотр корзины с неправильным методом. NEGATIVE")
@allure.description("Тест проверяет ошибку метода для просмотра корзины.")
@allure.severity("NORMAL")
@pytest.mark.api
@pytest.mark.negative
def test_get_cart_with_wrong_method(api_client: CartAPI) -> None:
    """
    Негативный тест: просмотр корзины с неправильным методом.

    :param api_client: API клиент
    :type api_client: CartAPI
    :return: None
    """
    with allure.step("Получить корзину неправильным методом"):
        result = api_client.get_cart_with_wrong_method()

    with allure.step("Проверить, что вернулась ошибка 405"):
        assert result.status_code == 405
