import json

from src.base_classes import AbstractFileWorker
from src.vacancies import Vacancy


class JSONWorker(AbstractFileWorker):
    def __init__(self, filename="data/vacancies.json"):
        self.__filename = filename

    def get_vacancy(self):
        """Читает вакансии из JSON-файла и возвращает генератор объектов Vacancy.

        Returns:
            Generator[Vacancy, None, None]: Генератор объектов вакансий.

        Note:
            Если файл не существует или содержит некорректный JSON, возвращает пустой генератор.
        """
        try:
            with open(self.__filename, "r", encoding="UTF-8") as f:
                vacancies = (Vacancy(**el) for el in json.load(f))
                return vacancies
        except FileNotFoundError:
            print(f"Файл {self.__filename} не найден")
            return (v for v in [])
        except json.JSONDecodeError:
            print(f"Файл {self.__filename} содержит некорректный JSON")
            return (v for v in [])

    def add_vacancy(self, vacancies: list[dict]) -> None:
        """Добавляет вакансии в JSON-файл, исключая дубликаты по названию.

        Args:
            vacancies: Список словарей с данными вакансий.

        Note:
            Если файл не существует, он будет создан.
            Вакансии с одинаковыми названиями не добавляются.
        """
        try:
            with open(self.__filename, "r", encoding="UTF-8") as f:
                cur_vacancies = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cur_vacancies = []

        for vacancy in vacancies:
            vacancy_name = vacancy.get("name")
            if vacancy_name and not any(vac.get("name") == vacancy_name for vac in cur_vacancies):
                cur_vacancies.append(vacancy)

        with open(self.__filename, "w", encoding="UTF-8") as f:
            json.dump(cur_vacancies, f, ensure_ascii=False, indent=4)

    def del_vacancy(self):
        """Очищает файл с вакансиями (удаляет все данные)."""
        with open(self.__filename, "w") as f:
            json.dump([], f)
