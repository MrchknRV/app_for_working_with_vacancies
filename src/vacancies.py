import re
from functools import total_ordering

from src.utils import get_convert_salary


@total_ordering
class Vacancy:
    """Класс для представления вакансии с валидацией данных и сравнением по зарплате.

    Позволяет:
    - Хранить информацию о вакансии (название, ссылка, зарплата, описание и т.д.).
    - Сравнивать вакансии по средней зарплате (через операторы `==`, `<` и ост.).
    - Валидировать URL-ссылку и конвертировать зарплату в рубли (если валюта другая).

    Attributes:
        name (str): Название вакансии.
        link (str): Ссылка на вакансию (URL).
        salary (int): Средняя зарплата в рублях (0 — если не указана).
        description (str): Описание вакансии или "Требования не указаны".
        area (str): Город/регион (приводится к формату с заглавной буквы).
        contact (str): Контактные данные для отклика.

    Raises:
        ValueError: Если передан некорректный URL.
    """

    __slots__ = ("name", "link", "salary", "description", "area", "contact")

    def __init__(self, name, link, salary, description, area, contact):
        """Инициализация вакансии.

        Args:
            name: Название вакансии.
            link: Ссылка на вакансию (должна быть валидным URL).
            salary: Словарь с данными о зарплате (ключи: 'from', 'to', 'currency').
            description: Текст с описанием вакансии.
            area: Город или регион.
            contact: Контактная информация.
        """
        self.name = name
        self._validate_link(link)
        self._validate_salary(salary)
        if isinstance(description, str):
            if description is not None:
                self.description = description
            else:
                self.description = "Требования не указаны."
        else:
            self.description = str(description)
        self.area = area.title()
        self.contact = contact

    def __str__(self):
        """Возвращает вакансию в виде читаемой строки (для вывода пользователю)."""
        return (
            f"Ищем {self.name} в {self.area}\nЗПшечка: {self.salary if self.salary != 0 else 'По договоренности!'}\n"
            f"Что нужно?\n{self.description}\n"
            f"Контакты: {self.contact}\n"
            f"Подробнее: {self.link}\n"
            f"Удачи!\n"
            f"{'-' * 10}"
        )

    def __eq__(self, other):
        """=="""
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return NotImplemented

    def __lt__(self, other):
        """<"""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    def _validate_link(self, link):
        """Проверяет, что ссылка валидна (формат URL).

        Args:
            link: Ссылка для проверки.

        Raises:
            ValueError: Если ссылка не соответствует формату URL.
        """
        if not isinstance(link, str):
            raise ValueError("Некорректный url-адрес")
        else:
            link_regex = r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"
            if bool(re.match(link_regex, link, re.IGNORECASE)):
                self.link = link
            else:
                raise ValueError("Некорректный url-адрес")

    def _validate_salary(self, salary: dict) -> None:
        """Конвертирует зарплату в рубли и вычисляет среднее значение.

        Если зарплата не указана, устанавливает 0. Конвертация валюты происходит через
        внешнюю функцию `get_convert_salary`.

        Args:
        """
        if salary:
            if salary["currency"] in ["RUR", "RUB"]:
                salary_from = salary["from"] if salary["from"] else 0
                salary_to = salary["to"] if salary["to"] else 0
                self.salary = (int(salary_from) + int(salary_to)) // 2
            else:
                salary_from = salary["from"] if salary["from"] else 0
                salary_to = salary["to"] if salary["to"] else 0
                self.salary = get_convert_salary((int(salary_from) + int(salary_to)) // 2, salary["currency"])
        else:
            self.salary = 0
