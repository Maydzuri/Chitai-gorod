import requests


def get_fresh_cookies() -> dict:
    """
    Получить свежие куки через API запрос

    :return: словарь с куками
    :rtype: dict
    """
    try:
        # Первый запрос для получения кук
        response = requests.get("https://www.chitai-gorod.ru/", timeout=10)
        cookies_dict = {}

        # Извлекаем нужные куки из ответа
        for cookie in response.cookies:
            if cookie.name.startswith('__ddg'):
                cookies_dict[cookie.name] = cookie.value

        # Если куки не получены, используем заглушку
        if not cookies_dict:
            cookies_dict = {'__ddg1': 'fallback_cookie_value'}

        return cookies_dict

    except Exception:
        # Fallback на случай ошибки
        return {'__ddg1': 'fallback_cookie_value'}
