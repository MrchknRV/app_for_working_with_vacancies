import json

from config import PATH
from src.vacancies import Vacancy
from src.vacancy_worker import JSONWorker

FILE = JSONWorker()


def greeting():
    print(
        """
        ╔════════════════════════════════════╗
        ║                                    ║
        ║   ДОБРО ПОЖАЛОВАТЬ В JOB FINDER!   ║
        ║                                    ║
        ╚════════════════════════════════════╝
        """
    )
    print(
        "Здесь вы можете легко находить подходящие вакансии, управлять избранными, фильтровать результаты и сохранять\n"
    )


def user_menu():
    print("Главное меню:")
    print("1. Поиск вакансий")
    print("2. Получить топ N вакансий по зарплате")
    print("3. Просмотр вакансий")
    print("4. Избранное")
    print("5. Очистить файл с вакансиями")
    print("6. Выйти")


def validate_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Пожалуйста, введите положительное число.")
                continue
            return value
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")


def iterate_vacancy(vacancies):
    if vacancies:
        favorite_vacancies = []
        i = 0
        while i < len(vacancies):
            print("\nТЕКУЩАЯ ВАКАНСИЯ:")
            print(Vacancy(**vacancies[i]))
            user_choice = input(
                "\nВыберите действие:\n"
                "1 - Добавить вакансию в избранное\n"
                "2 - Просмотреть следующую вакансию\n"
                "3 - Выйти\n"
                "> "
            ).strip()
            if user_choice == "1":
                FILE.add_vacancy([vacancies[i]])
                favorite_vacancies.append(vacancies[i])
                i += 1
            elif user_choice == "2":
                i += 1
            elif user_choice == "3":
                break
            else:
                print("Неверный ввод, попробуйте еще раз")
        with open(PATH / "data" / "likes_vacancy.json", "w", encoding="UTF-8") as f:
            json.dump(favorite_vacancies, f, ensure_ascii=False, indent=4)


def save_vacancies(vacancies):
    user_input = input("\nЖелаете сохранить все вакансии(да/нет):\n> ").lower().strip()
    if user_input == "да":
        FILE.add_vacancy(vacancies)
        print("Вакансии сохранены")
    else:
        print("Вакансии не сохранены")


def viewing_favorites(filepath):
    with open(filepath, encoding="UTF-8") as f:
        return json.load(f)
