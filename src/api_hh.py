import requests

from src.base_classes import HeadHunterAPI


class HH(HeadHunterAPI):
    """Класс для взаимодействия с API HeadHunter (hh.ru).

    Позволяет:
    - Подключаться к API hh.ru и получать вакансии по заданным параметрам.
    - Обрабатывать ответы API (включая проверку ошибок и валидацию данных).
    - Пагинировать результаты (получать вакансии с нескольких страниц).

    Attributes:
        __url (str): Базовый URL API HeadHunter.
        __params (dict): Параметры запроса по умолчанию.
        __vacancies (list): Список для хранения полученных вакансий.

    Inherits:
        HeadHunterAPI: Базовый класс API.
    """

    def __init__(self):
        """Инициализирует подключение к API hh.ru.

        Устанавливает:
        - Базовый URL API.
        - Параметры запроса по умолчанию:
            * text: Пустая строка (поисковый запрос).
            * page: 0 (начальная страница).
            * per_page: 100 (количество вакансий на странице).
            * area: ["113"] (регион "Россия").
        - Пустой список для хранения вакансий.
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"text": "", "page": 0, "per_page": 100, "area": ["113"]}
        self.__vacancies = []
        super().__init__()

    def _api_connect(self, params: str = ""):
        """Устанавливает соединение с API hh.ru и возвращает ответ.

        Args:
            params: Поисковый запрос (например, "Python разработчик").

        Returns:
            Response: Объект ответа от API.

        Raises:
            requests.HTTPError: Если запрос к API завершился ошибкой (статус != 200).
        """
        self.__params["text"] = params
        response = requests.get(self.__url, params=self.__params)
        response.raise_for_status()
        return response

    def get_vacancies(self, text="", page: int = 5):
        """Возвращает список вакансий по заданному поисковому запросу.

        Запрашивает вакансии с указанного количества страниц (по умолчанию — 5).

        Args:
            text: Поисковый запрос (например, "Data Scientist").
            page: Количество страниц для парсинга (по умолчанию 5).

        Returns:
            list[dict]: Список вакансий в формате JSON.

        Raises:
            ValueError: Если ответ от сервера пустой.
            KeyError: Если в ответе отсутствует ключ 'items'.
        """
        while self.__params["page"] < page:
            response = self._api_connect(text)
            if response.text:
                try:
                    data = response.json()
                except ValueError:
                    print("Invalid JSON data.")
                    break

                if "items" not in data:
                    raise KeyError("Ключ 'items' отсутствует.")

                for vacancy in data["items"]:
                    self.__vacancies.append({
                        "name": vacancy["name"],
                        "link": vacancy["alternate_url"],
                        "salary": vacancy["salary"],
                        "description": vacancy["snippet"]["requirement"],
                        "area": vacancy["area"]["name"],
                        "contact": vacancy["department"]["name"] if vacancy["department"] else "Не указано."
                    })
            else:
                raise ValueError("An empty response from the server")
            self.__params["page"] += 1
        return self.__vacancies
