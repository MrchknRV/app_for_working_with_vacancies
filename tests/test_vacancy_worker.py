import json
from unittest.mock import patch

import pytest

from src.vacancy_worker import JSONWorker


@pytest.fixture
def sample_vacancies():
    return [{"name": "Python Developer", "salary": "100000"}, {"name": "Data Scientist", "salary": "120000"}]


@pytest.fixture
def duplicate_vacancies():
    return [{"name": "Python Developer", "salary": "110000"}]  # Дубликат по имени


@pytest.fixture
def json_worker(tmp_path):
    test_file = tmp_path / "vacancies.json"
    return JSONWorker(filename=test_file)


def test_get_vacancy_file_not_found(json_worker, capsys):
    """Тестирование получения вакансий из несуществующего файла"""
    result = list(json_worker.get_vacancy())
    assert len(result) == 0
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_get_vacancy_invalid_json(tmp_path, capsys):
    """Тестирование обработки некорректного JSON"""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}")

    worker = JSONWorker(filename=test_file)
    result = list(worker.get_vacancy())
    assert len(result) == 0
    captured = capsys.readouterr()
    assert "содержит некорректный JSON" in captured.out


def test_add_vacancy_to_new_file(json_worker, sample_vacancies):
    """Тестирование добавления вакансий в новый файл"""
    json_worker.add_vacancy(sample_vacancies)

    with open(json_worker._JSONWorker__filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["name"] == "Python Developer"


def test_add_vacancy_no_duplicates(json_worker, sample_vacancies, duplicate_vacancies):
    """Тестирование предотвращения дубликатов"""
    json_worker.add_vacancy(sample_vacancies)
    json_worker.add_vacancy(duplicate_vacancies)

    with open(json_worker._JSONWorker__filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == 2  # Дубликат не добавлен
        # Проверяем что зарплата не обновилась
        assert data[0]["salary"] == "100000"


def test_clear_vacancies(json_worker, sample_vacancies):
    """Тестирование очистки файла"""
    json_worker.add_vacancy(sample_vacancies)
    json_worker.clear_vacancies()

    with open(json_worker._JSONWorker__filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == 0


@pytest.mark.parametrize(
    "key,value,expected_count", [("name", "Python", 1), ("salary", "120000", 1), ("name", "Java", 2), (None, None, 2)]
)
def test_del_vacancy(json_worker, sample_vacancies, key, value, expected_count):
    """Тестирование удаления вакансий по ключу и значению"""
    json_worker.add_vacancy(sample_vacancies)
    json_worker.del_vacancy(key_word=key, value_word=value)

    with open(json_worker._JSONWorker__filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == expected_count


def test_del_vacancy_error_handling(json_worker, capsys):
    """Тестирование обработки ошибок при удалении"""
    with patch("builtins.open", side_effect=Exception("Test error")):
        json_worker.del_vacancy(key_word="name", value_word="Python")
        captured = capsys.readouterr()
        assert "Произошла ошибка" in captured.out


def test_add_vacancy_file_creation(tmp_path):
    """Тестирование создания файла при добавлении вакансий"""
    test_file = tmp_path / "new_vacancies.json"
    assert not test_file.exists()

    worker = JSONWorker(filename=test_file)
    worker.add_vacancy([{"name": "Test", "salary": "50000"}])

    assert test_file.exists()
    with open(test_file, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == 1


def test_case_insensitive_deletion(json_worker, sample_vacancies):
    """Тестирование регистронезависимого удаления"""
    json_worker.add_vacancy(sample_vacancies)
    json_worker.del_vacancy(key_word="name", value_word="python")

    with open(json_worker._JSONWorker__filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Data Scientist"
