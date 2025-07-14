from abc import ABC
from unittest.mock import Mock

import pytest

from src.base_classes import AbstractFileWorker, HeadHunterAPI


def test_headhunterapi_is_abstract():
    """Проверяет, что HeadHunterAPI является абстрактным классом."""
    assert issubclass(HeadHunterAPI, ABC)

    with pytest.raises(TypeError) as excinfo:
        HeadHunterAPI()
    assert "Can't instantiate abstract class" in str(excinfo.value)


def test_headhunterapi_abstract_methods():
    """Проверяет наличие абстрактных методов в HeadHunterAPI."""
    assert "_api_connect" in HeadHunterAPI.__dict__
    assert "get_vacancies" in HeadHunterAPI.__dict__


def test_abstractfileworker_is_abstract():
    """Проверяет, что AbstractFileWorker является абстрактным классом."""
    assert issubclass(AbstractFileWorker, ABC)

    with pytest.raises(TypeError) as excinfo:
        AbstractFileWorker()
    assert "Can't instantiate abstract class" in str(excinfo.value)


def test_abstractfileworker_abstract_methods():
    """Проверяет наличие абстрактных методов в AbstractFileWorker."""
    assert "add_vacancy" in AbstractFileWorker.__abstractmethods__
    assert "clear_vacancies" in AbstractFileWorker.__abstractmethods__
    assert "get_vacancy" in AbstractFileWorker.__abstractmethods__
    assert "del_vacancy" in AbstractFileWorker.__abstractmethods__


def test_concrete_implementation_hh_api():
    """Проверяет корректную реализацию класса-наследника HeadHunterAPI."""

    class ConcreteHHAPI(HeadHunterAPI):
        def _api_connect(self, *args, **kwargs):
            return Mock()

        def get_vacancies(self, *args, **kwargs):
            return []

    instance = ConcreteHHAPI()
    assert isinstance(instance._api_connect(), Mock)
    assert instance.get_vacancies() == []


def test_concrete_implementation_file_worker():
    """Проверяет корректную реализацию класса-наследника AbstractFileWorker."""

    class ConcreteFileWorker(AbstractFileWorker):
        def add_vacancy(self, *args, **kwargs):
            return True

        def clear_vacancies(self, *args, **kwargs):
            return True

        def get_vacancy(self, *args, **kwargs):
            return []

        def del_vacancy(self, *args, **kwargs):
            return True

    instance = ConcreteFileWorker()
    assert instance.add_vacancy() is True
    assert instance.clear_vacancies() is True
    assert instance.get_vacancy() == []
    assert instance.del_vacancy() is True


def test_docstrings_presence():
    """Проверяет наличие docstring у абстрактных классов и методов."""
    assert HeadHunterAPI.__doc__
    assert HeadHunterAPI._api_connect.__doc__
    assert HeadHunterAPI.get_vacancies.__doc__

    assert AbstractFileWorker.__doc__
    assert AbstractFileWorker.add_vacancy.__doc__
    assert AbstractFileWorker.clear_vacancies.__doc__
    assert AbstractFileWorker.get_vacancy.__doc__
    assert AbstractFileWorker.del_vacancy.__doc__
