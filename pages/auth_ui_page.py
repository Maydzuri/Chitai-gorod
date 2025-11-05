from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:
    """
    Page Object для формы авторизации.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация формы авторизации.
        :param driver: WebDriver - Экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.login_button = (
            By.CSS_SELECTOR,
            "button.header-controls__btn[aria-label='Меню профиля']"
        )
        self.phone_input = (By.CSS_SELECTOR, "input#tid-input")
        self.get_code_button = (
            By.CSS_SELECTOR,
            "button.auth-modal-content__button"
        )

    def open_auth_form(self) -> None:
        """
        Открыть форму авторизации нажатием на кнопку входа.
        :return: None
        """
        login_btn = self.driver.find_element(*self.login_button)
        login_btn.click()

    def enter_phone_number(self, phone: str) -> None:
        """
        Ввести номер телефона в поле ввода.
        :param phone: номер телефона для ввода (str)
        :return: None
        """
        phone_field = self.wait.until(
            EC.presence_of_element_located(self.phone_input)
        )
        phone_field.clear()
        phone_field.send_keys(phone)
