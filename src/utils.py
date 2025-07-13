from src.vacancies import Vacancy

# logger = logging.getLogger(__name__)
# file_handler = logging.FileHandler(PATH / "logs" / "logging.log", "w", encoding="UTF-8")
# file_formatter = logging.Formatter(
#     "[%(asctime)s.%(msecs)03d] [%(levelname)-7s] - %(name)r - (%(filename)s).%(funcName)s:%(lineno)-3d - %(message)s"
# )
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)
# logger.setLevel(logging.DEBUG)


def get_top_vacancies_for_salary(vacancies: list[dict], top: int = 5) -> list[Vacancy]:
    """
    Возвращает топ N вакансий по зарплате (по убыванию).

    Параметры:
        vacancies (List[dict]): Список вакансий в виде словарей.
        top (int): Количество возвращаемых вакансий (по умолчанию 5).

    Возвращает:
        List[Vacancy]: Топ N вакансий, отсортированных по зарплате (от высокой к низкой).

    Пример:
        >>> vacancies = [{"salary_from": 100, "salary_to": 200}, {"salary_from": 150, "salary_to": 300}]
        >>> top_vacancies = get_top_vacancies_for_salary(vacancies, top=2)
        >>> len(top_vacancies)
        2
    """
    transform_list = [Vacancy(**vac) for vac in vacancies]
    return sorted(transform_list, reverse=True)[:top]


# def get_filtered_vacancies_for_str(vacancies: list[dict], search_word: str = None) -> list[dict]:
#     """Функция принимает список словарей с данными о вакансиях, строку поиска и ключ поиска,
#     а возвращает список словарей, у которых в описании есть данная строка."""
#     try:
#         if not search_word:
#             return vacancies
#         if len(vacancies) > 0:
#             filtered_vacancies = []
#             for vacancy in vacancies:
#                 if search_word in vacancy['description']:
#                     filtered_vacancies.append(vacancy)
#             return filtered_vacancies
#         return []
#     except Exception as exc:
#         print(f"Произошла ошибка {exc}")
#     return []
