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

    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def del_vacancy(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_vacancy(self, *args, **kwargs):
        raise NotImplementedError
