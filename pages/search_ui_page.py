from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    """
    Page Object для страницы поиска товаров.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы поиска.
        :param driver: WebDriver - Экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Локаторы для поисковой строки
        self.search = (
            By.CSS_SELECTOR,
            "input[type='search'], .search-form__input, [name='q']"
        )
        self.search_button = (
            By.CSS_SELECTOR,
            "button.search-form__button-search"
        )

        # Локаторы для результатов поиска
        self.search_results = (
            By.CSS_SELECTOR,
            ".product-card, .catalog-product, [data-product-id]"
        )
        self.product_titles = (By.CSS_SELECTOR, ".product-card__title")

    def search_by_title(self, book_title: str) -> None:
        """
        Выполнить поиск книги по названию.
        :param book_title: название книги для поиска (str)
        :return: None
        """
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.search)
        )
        search_input.clear()
        search_input.send_keys(book_title)

        search_button = self.driver.find_element(*self.search_button)
        search_button.click()

        # Ожидание изменения URL на страницу результатов
        WebDriverWait(self.driver, 10).until(
            lambda d: "search" in d.current_url or "phrase" in d.current_url
        )
        # Ожидание полной загрузки страницы
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )
        # Ожидание появления контейнеров товаров
        self.wait.until(
            EC.presence_of_element_located(self.search_results)
        )
        # Ожидание появления заголовков товаров
        self.wait.until(
            EC.presence_of_all_elements_located(self.product_titles)
        )

    def search_negative(self, book_title: str) -> None:
        """
        Выполнить поиск по несуществующему названию.
        :param book_title: название книги для поиска (str)
        :return: None
        """
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.search)
        )
        search_input.clear()
        search_input.send_keys(book_title)

        search_input.send_keys(Keys.ENTER)

        # Ожидание полной загрузки страницы
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )
