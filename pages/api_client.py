import requests
from cookie_helper import get_fresh_cookies
from config import url_api, bearer_token


class CartAPI:
    """
    API клиент для работы с корзиной.
    """

    def __init__(self) -> None:
        """
        Инициализация API клиента со свежими куками.
        """
        self.base_url = url_api
        self.session = requests.Session()

        # Получаем свежие куки
        self._update_cookies()

        # Базовые заголовки
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36',
            'Authorization': bearer_token
        })

    def _update_cookies(self) -> None:
        """
        Обновить куки сессии.

        :return: None
        """
        fresh_cookies = get_fresh_cookies()
        self.session.cookies.update(fresh_cookies)

    def add_product_to_cart(self, product_id: int) -> requests.Response:
        """
        Добавить товар в корзину.

        :param product_id: ID товара
        :type product_id: int
        :return: Response object
        :rtype: requests.Response
        """
        self._update_cookies()

        url = f"{self.base_url}/product"
        payload = {
            "id": product_id
        }
        resp = self.session.post(url, json=payload)
        return resp

    def add_product_without_id(self) -> requests.Response:
        """
        Добавить товар без ID.

        :return: Response object
        :rtype: requests.Response
        """
        self._update_cookies()

        url = f"{self.base_url}/product"
        resp = self.session.post(url)
        return resp

    def get_cart(self) -> requests.Response:
        """
        Получить содержимое корзины.

        :return: Response object
        :rtype: requests.Response
        """
        self._update_cookies()

        resp = self.session.get(self.base_url)
        return resp

    def remove_from_cart(self, cart_product_id: int) -> requests.Response:
        """
        Удалить товар из корзины.

        :param cart_product_id: ID товара в корзине (поле "id" из ответа)
        :type cart_product_id: int
        :return: Response object
        :rtype: requests.Response
        """
        self._update_cookies()

        url = f"{self.base_url}/product/{cart_product_id}"
        resp = self.session.delete(url)
        return resp

    def get_cart_with_wrong_method(self) -> requests.Response:
        """
        Просмотр товаров в корзине с неправильным методом (POST вместо GET).

        :return: Response object
        :rtype: requests.Response
        """
        self._update_cookies()

        # Используем POST вместо GET для негативного теста
        resp = self.session.post(self.base_url)
        return resp
