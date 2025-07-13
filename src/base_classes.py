from abc import ABC, abstractmethod


class HeadHunterAPI(ABC):
    """
    Абстрактный класс для работы с API.

    Класс содержит методы, которые будут реализованы в классах наследниках.
    """

    @abstractmethod
    def _api_connect(self, *args, **kwargs):
        """Метод подключения к API"""
        raise NotImplementedError

    def get_vacancies(self, *args, **kwargs):
        """Метод получения вакансий"""
        raise NotImplementedError


class AbstractFileWorker(ABC):
    """Абстрактный базовый класс для работы с хранилищем вакансий.

    Определяет обязательный интерфейс для классов, работающих с различными
    типами хранилищ (JSON, CSV, базы данных и т.д.).

    Все наследующие классы должны реализовать три основных метода:
    - добавление вакансий
    - удаление вакансий
    - получение вакансий

    Methods:
        add_vacancy: Добавляет вакансии в хранилище.
        del_vacancy: Удаляет вакансии из хранилища.
        get_vacancy: Возвращает вакансии из хранилища.
    """

    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        """Добавляет вакансии в хранилище.

        Args:
            *args: Позиционные аргументы для реализации в дочерних классах.
            **kwargs: Именованные аргументы для реализации в дочерних классах.

        Raises:
            NotImplementedError: Если метод не реализован в дочернем классе.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_vacancies(self, *args, **kwargs):
        """Удаляет вакансии из хранилища.

        Args:
            *args: Позиционные аргументы для реализации в дочерних классах.
            **kwargs: Именованные аргументы для реализации в дочерних классах.

        Raises:
            NotImplementedError: Если метод не реализован в дочернем классе.
        """
        raise NotImplementedError

    @abstractmethod
    def get_vacancy(self, *args, **kwargs):
        """Возвращает вакансии из хранилища.

        Args:
            *args: Позиционные аргументы для реализации в дочерних классах.
            **kwargs: Именованные аргументы для реализации в дочерних классах.

        Returns:
            Generator: Генератор объектов вакансий.

        Raises:
            NotImplementedError: Если метод не реализован в дочернем классе.
        """
        raise NotImplementedError

    @abstractmethod
    def del_vacancy(self, *args, **kwargs):
        raise NotImplementedError
