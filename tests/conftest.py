import pytest

from src.vacancy_worker import JSONWorker


@pytest.fixture
def sample_vacancies():
    return [
        {
            "name": "Python Developer",
            "link": "http://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Опыт работы 3+ года",
            "area": "Москва",
            "contact": "hr@example.com",
        },
        {
            "name": "Data Scientist",
            "link": "http://example.com/ds",
            "salary": None,
            "description": "Знание Python и ML",
            "area": "Санкт-Петербург",
            "contact": None,
        },
    ]


@pytest.fixture
def json_worker(tmp_path):
    test_file = tmp_path / "test_vacancies.json"
    return JSONWorker(file_path=test_file)


@pytest.fixture
def likes_file(tmp_path):
    return tmp_path / "likes_vacancy.json"
