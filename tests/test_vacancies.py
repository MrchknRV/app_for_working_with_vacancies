from unittest.mock import patch

import pytest

from src.vacancies import Vacancy


@pytest.fixture
def sample_vacancy():
    """Фикстура для создания тестовой вакансии."""
    return Vacancy(
        name="Python Developer",
        link="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Опыт работы 3+ года",
        area="Москва",
        contact="hr@example.com",
    )


@pytest.fixture
def vacancy_no_salary():
    """Фикстура для вакансии без указания зарплаты."""
    return Vacancy(
        name="Intern",
        link="https://intern.com",
        salary=None,
        description="Обучение Python",
        area="Санкт-Петербург",
        contact=None,
    )


def test_vacancy_initialization(sample_vacancy):
    """Проверяет корректность инициализации вакансии."""
    assert sample_vacancy.name == "Python Developer"
    assert sample_vacancy.link == "https://example.com"
    assert sample_vacancy.salary == 125000
    assert sample_vacancy.description == "Опыт работы 3+ года"
    assert sample_vacancy.area == "Москва"
    assert sample_vacancy.contact == "hr@example.com"


def test_vacancy_no_salary(vacancy_no_salary):
    """Проверяет инициализацию вакансии без зарплаты."""
    assert vacancy_no_salary.salary == 0
    assert vacancy_no_salary.description == "Обучение Python"


def test_vacancy_str(sample_vacancy, vacancy_no_salary):
    """Проверяет строковое представление вакансии."""
    assert "Python Developer" in str(sample_vacancy)
    assert "ЗПшечка: 125000" in str(sample_vacancy)
    assert "По договоренности!" in str(vacancy_no_salary)


def test_vacancy_equality(sample_vacancy):
    """Проверяет сравнение вакансий по зарплате (==)."""
    same_salary_vacancy = Vacancy(
        name="Java Developer",
        link="https://java.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Опыт работы 3+ года",
        area="Москва",
        contact="hr@java.com",
    )
    assert sample_vacancy == same_salary_vacancy


def test_vacancy_less_than(sample_vacancy, vacancy_no_salary):
    """Проверяет сравнение вакансий по зарплате (<)."""
    higher_salary_vacancy = Vacancy(
        name="Senior Python Developer",
        link="https://senior.com",
        salary={"from": 200000, "to": 250000, "currency": "RUR"},
        description="Опыт работы 5+ лет",
        area="Москва",
        contact="hr@senior.com",
    )
    assert sample_vacancy < higher_salary_vacancy
    assert vacancy_no_salary < sample_vacancy


def test_invalid_link():
    """Проверяет валидацию некорректной ссылки."""
    with pytest.raises(ValueError, match="Некорректный url-адрес"):
        Vacancy(
            name="Invalid Link",
            link="not-a-url",
            salary={"from": 50000, "to": 70000, "currency": "RUR"},
            description="Invalid URL test",
            area="Москва",
            contact=None,
        )


@patch("src.vacancies.get_convert_salary")
def test_foreign_currency_salary(mock_convert, sample_vacancy):
    """Проверяет конвертацию зарплаты в иностранной валюте."""
    mock_convert.return_value = 750000
    usd_vacancy = Vacancy(
        name="Python Developer (USD)",
        link="https://usd.com",
        salary={"from": 10000, "to": 12000, "currency": "USD"},
        description="Опыт работы 3+ года",
        area="Нью-Йорк",
        contact="hr@usd.com",
    )
    assert usd_vacancy.salary == 750000
    mock_convert.assert_called_once_with(11000, "USD")


def test_salary_with_only_from():
    """Проверяет расчет зарплаты, если указана только нижняя граница."""
    vacancy = Vacancy(
        name="Python Dev (from only)",
        link="https://from.com",
        salary={"from": 80000, "to": None, "currency": "RUR"},
        description="Only from salary",
        area="Москва",
        contact=None,
    )
    assert vacancy.salary == 40000


def test_salary_with_only_to():
    """Проверяет расчет зарплаты, если указана только верхняя граница."""
    vacancy = Vacancy(
        name="Python Dev (to only)",
        link="https://to.com",
        salary={"from": None, "to": 120000, "currency": "RUR"},
        description="Only to salary",
        area="Москва",
        contact=None,
    )
    assert vacancy.salary == 60000
