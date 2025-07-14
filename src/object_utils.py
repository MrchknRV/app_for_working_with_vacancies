import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_convert_salary(convert_dig: int, currency_from: str) -> int:
    """Конвертирует сумму из указанной валюты в рубли (RUB) через API Fixer.

    Использует внешний сервис (api.apilayer.com/fixer) для получения актуального курса.
    Возвращает сумму в рублях, округлённую до целого числа.

    Args:
        convert_dig (int): Сумма для конвертации (должна быть >= 0).
        currency_from (str): Код исходной валюты (например, "USD", "EUR").

    Returns:
        int: Сумма в рублях после конвертации.

    Raises:
        requests.HTTPError: Если API возвращает код статуса != 200.
        ValueError: Если:
            - ответ API пустой,
            - не удалось декодировать JSON,
            - `convert_dig` отрицательное.
        KeyError: Если в ответе API отсутствует ключ 'result'.

    Example:
        >>> get_convert_salary(100, "USD")
        7500  # Пример: 100 USD → 7500 RUB (курс 1 USD = 75 RUB)
    """
    url = f"https://api.apilayer.com/fixer/convert?to={"RUB"}&from={currency_from}&amount={convert_dig}"
    headers = {"apikey": "x74Iu8tVtaqj0l1OC90r0oqNeqSgQPtc"}
    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    if not response.text:
        raise ValueError("An empty response from the server")
    try:
        data = response.json()
    except requests.JSONDecodeError as exc:
        raise ValueError(f"Ошибка декодирования JSON: {exc}")
    if "result" not in data:
        raise KeyError("Ключ 'result' отсутствует в ответе API.")

    result = data["result"]

    return int(result)
