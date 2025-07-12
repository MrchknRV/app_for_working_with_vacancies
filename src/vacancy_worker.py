import json

from src.base_classes import AbstractFileWorker
from src.vacancies import Vacancy


class JSONWorker(AbstractFileWorker):
    def __init__(self, filename="data/vacancies.json"):
        self.__filename = filename

    def get_vacancy(self):
        try:
            with open(self.__filename, "r", encoding="UTF-8") as f:
                vacancies = (Vacancy(**el) for el in json.load(f))
                return vacancies
        except FileNotFoundError:
            print("Файл не найден")
            return []
        except json.JSONDecodeError:
            return []

    def add_vacancy(self, vacancies: list[dict]):
        with open(self.__filename, encoding="UTF-8") as f:
            cur_vacancies = json.load(f)
        for vacancy in vacancies:
            vacancy_name = vacancy["name"]
            if not any(vac["name"] == vacancy_name for vac in cur_vacancies):
                cur_vacancies.append(vacancy)
            continue
        with open(self.__filename, "w", encoding="UTF-8") as f:
            json.dump(cur_vacancies, f, ensure_ascii=False, indent=4)

    def del_vacancy(self, key):
        with open(self.__filename, "w") as f:
            json.dump([], f)
