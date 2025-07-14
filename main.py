from config import PATH
from src.api_hh import HH
from src.main_utils import (greeting, iterate_vacancy, save_vacancies, user_menu, validate_integer_input,
                            viewing_favorites)
from src.utils import get_top_vacancies_for_salary
from src.vacancy_worker import JSONWorker

# HUNTER_VAC = HH()
# MENU = {}
WORK_FILE = JSONWorker()


def main():
    greeting()
    hunter_vac = HH()
    while True:
        user_menu()
        user_input = input("Введите номер опции:\n> ").strip()

        if user_input == "1":
            param_text = input("\nВведите ключевое слово для поиска вакансий:\n> ")

            try:
                vacancies = hunter_vac.get_vacancies(param_text)
                if not vacancies:
                    print("Вакансии не найдены")
                iterate_vacancy(vacancies)
                save_vacancies(vacancies)

            except Exception as exc:
                print(f"{exc}")
                break

        elif user_input == "2":
            user_input = input("\n1. Сохраненные вакансии\n" "2. Новые вакансии\n" "3. Назад\n").strip()
            if user_input == "1":
                vacancies = WORK_FILE.get_vacancy()
                try:
                    if vacancies:
                        top_vacancies = get_top_vacancies_for_salary(vacancies)
                        for vac in top_vacancies:
                            print(str(vac))
                    else:
                        print("Нет доступных вакансий, давайте найдем!")
                except Exception:
                    print("Ошибка! Попробуйте ещё раз")
            elif user_input == "2":
                top = validate_integer_input("Введите количество топ вакансий по зарплате: ")
                param_text = input("\nВведите ключевое слово для поиска вакансий:(Оставьте пустым для любых)\n> ")
                try:
                    vacancies = hunter_vac.get_vacancies(param_text)
                    top_vacancies = get_top_vacancies_for_salary(vacancies, top)
                    for vac in top_vacancies:
                        print(str(vac))
                except Exception:
                    print("Ошибка! Попробуйте ещё раз")
            else:
                pass

        elif user_input == "3":
            vacancies = WORK_FILE.get_vacancy()
            iterate_vacancy(vacancies)
        elif user_input == "4":
            filedir = PATH / "data" / "likes_vacancy.json"
            vacancies = viewing_favorites(filedir)
            iterate_vacancy(vacancies)
        elif user_input == "5":
            WORK_FILE.clear_vacancies()

        elif user_input == "6":
            print("Выход из программы")
            break


if __name__ == "__main__":
    main()
