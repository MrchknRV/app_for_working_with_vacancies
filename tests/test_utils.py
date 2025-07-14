from src.utils import get_top_vacancies_for_salary


def test_get_top_vacancies_empty_input():
    """Проверяет обработку пустого списка вакансий."""
    assert get_top_vacancies_for_salary([]) == []
