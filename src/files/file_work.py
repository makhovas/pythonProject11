from abc import ABC, abstractmethod
from src.app.vacancies import Vacancy
import csv
from typing import Dict, Any, List
import json


class BaseFileHandler(ABC):
    """Абстрактный базовый класс для обработки файлов"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод для добавления вакансии в файл.

        :param vacancy: Вакансия для добавления.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: str) -> List[Vacancy]:
        """
        Абстрактный метод для получения вакансий из файла по заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод для удаления вакансии из файла.

        :param vacancy: Вакансия для удаления.
        """
        pass


class CSVFileHandler(BaseFileHandler):
    """Класс для обработки CSV файлов с вакансиями"""

    def __init__(self, file_path: str):
        """
        Инициализация объекта CSVFileHandler.

        :param file_path: Путь к CSV файлу.
        """
        self.file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в CSV файл.

        :param vacancy: Вакансия для добавления.
        """
        with open(self.file_path, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                vacancy.title,
                vacancy.link,
                vacancy.salary,
                vacancy.date
            ])

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Возвращает список вакансий из CSV файла, соответствующих заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        vacancies = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                vacancy_data = {
                    "title": row[0],
                    "link": row[1],
                    "salary": row[2],
                    "date": row[3]
                }
                if self._vacancy_matches_criteria(vacancy_data, criteria):
                    vacancies.append(vacancy_data)
        return vacancies

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из CSV файла.

        :param vacancy: Вакансия для удаления.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open(self.file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(rows[0])
            for row in rows[1:]:
                vacancy_data = {
                    "title": row[0],
                    "link": row[1],
                    "salary": row[2],
                    "date": row[3]
                }
                if not self._vacancy_equals(vacancy_data, vacancy):
                    writer.writerow(row)

    @staticmethod
    def _vacancy_matches_criteria(vacancy_data: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Проверяет, соответствует ли вакансия заданным критериям.

        :param vacancy_data: Данные вакансии.
        :param criteria: Критерии для проверки.
        :return: True, если вакансия соответствует критериям, иначе False.
        """
        for key, value in criteria.items():
            if key not in vacancy_data or vacancy_data[key] != value:
                return False
        return True

    @staticmethod
    def _vacancy_equals(vacancy_data1: Dict[str, Any], vacancy_data2: Dict[str, Any]) -> bool:
        """
        Проверяет, являются ли две вакансии одинаковыми.

        :param vacancy_data1: Данные первой вакансии.
        :param vacancy_data2: Данные второй вакансии.
        :return: True, если вакансии равны, иначе False.
        """
        return vacancy_data1 == vacancy_data2


class JSONFileHandler(BaseFileHandler):
    """Класс для обработки JSON файлов с вакансиями"""

    def __init__(self, file_path: str):
        """
        Инициализация объекта JSONFileHandler.

        :param file_path: Путь к JSON файлу.
        """
        self.file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в JSON файл.

        :param vacancy: Вакансия для добавления.
        """
        with open(self.file_path, "a", encoding="utf-8") as file:
            vacancy_dict = {
                "title": vacancy.title,
                "link": vacancy.link,
                "salary": vacancy.salary,
                "date": vacancy.date
            }
            json.dump(vacancy_dict, file, ensure_ascii=False)
            file.write("\n")

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Возвращает список вакансий из JSON файла, соответствующих заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        vacancies = []
        with open(self.file_path, "r") as file:
            for line in file:
                vacancy_data = json.loads(line)
                if self._vacancy_matches_criteria(vacancy_data, criteria):
                    vacancies.append(vacancy_data)
        return vacancies

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из JSON файла.

        :param vacancy: Вакансия для удаления.
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        with open(self.file_path, "w") as file:
            for line in lines:
                vacancy_data = json.loads(line)
                if not self._vacancy_equals(vacancy_data, vacancy):
                    file.write(line)

    @staticmethod
    def _vacancy_matches_criteria(vacancy_data: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Проверяет, соответствует ли вакансия заданным критериям.

        :param vacancy_data: Данные вакансии.
        :param criteria: Критерии для проверки.
        :return: True, если вакансия соответствует критериям, иначе False.
        """
        for key, value in criteria.items():
            if key not in vacancy_data or vacancy_data[key] != value:
                return False
        return True

    @staticmethod
    def _vacancy_equals(vacancy_data1: Dict[str, Any], vacancy_data2: Dict[str, Any]) -> bool:
        """
        Проверяет, являются ли две вакансии одинаковыми.

        :param vacancy_data1: Данные первой вакансии.
        :param vacancy_data2: Данные второй вакансии.
        :return: True, если вакансии равны, иначе False.
        """
        return vacancy_data1 == vacancy_data2
