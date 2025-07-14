import json

import pytest

from src.main_utils import greeting, user_menu, validate_integer_input


def test_greeting(capsys):
    greeting()
    captured = capsys.readouterr()
    assert "ДОБРО ПОЖАЛОВАТЬ В JOB FINDER!" in captured.out


def test_user_menu(capsys):
    user_menu()
    captured = capsys.readouterr()
    assert "1. Поиск вакансий" in captured.out
    assert "6. Выйти" in captured.out


def test_validate_integer_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")
    assert validate_integer_input("Введите число: ") == 5

    inputs = iter(["abc", "0", "-5", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert validate_integer_input("Введите число: ") == 10


@pytest.mark.parametrize("input_value,expected", [("5", 5), ("10", 10)])
def test_validate_integer_input_valid(input_value, expected, monkeypatch):
    from main import validate_integer_input

    monkeypatch.setattr("builtins.input", lambda _: input_value)
    assert validate_integer_input("Введите число: ") == expected


@pytest.mark.parametrize("input_values", [(["abc", "5"]), (["-5", "10"]), (["0", "15"])])
def test_validate_integer_input_invalid(input_values, monkeypatch):
    from main import validate_integer_input

    input_iter = iter(input_values)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    assert validate_integer_input("Введите число: ") == int(input_values[-1])


def test_viewing_favorites(sample_vacancies, tmp_path):
    from main import viewing_favorites

    test_file = tmp_path / "test_favorites.json"

    with open(test_file, "w", encoding="UTF-8") as f:
        json.dump([sample_vacancies[0]], f, ensure_ascii=False, indent=4)

    result = viewing_favorites(test_file)
    assert len(result) == 1
    assert result[0]["name"] == "Python Developer"


def test_viewing_favorites_file_not_found(tmp_path):
    from main import viewing_favorites

    test_file = tmp_path / "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        viewing_favorites(test_file)
