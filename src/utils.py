from dotenv import load_dotenv

from src.vacancies import Vacancy

# logger = logging.getLogger(__name__)
# file_handler = logging.FileHandler(PATH / "logs" / "logging.log", "w", encoding="UTF-8")
# file_formatter = logging.Formatter(
#     "[%(asctime)s.%(msecs)03d] [%(levelname)-7s] - %(name)r - (%(filename)s).%(funcName)s:%(lineno)-3d - %(message)s"
# )
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)
# logger.setLevel(logging.DEBUG)

load_dotenv()


def get_top_vacancies_for_salary(vacancies: list[dict], top: int = 5) -> list[Vacancy]:
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
