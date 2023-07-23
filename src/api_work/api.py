from abc import ABC, abstractmethod
import requests
import os


class API(ABC):
    def __init__(self, base_url: str, number_of_vacancies: int = 100):
        """
        Инициализация базового класса для API.

        :param base_url: Базовый URL для API.
        :param number_of_vacancies: Количество вакансий для получения.
        """
        self._base_url = base_url
        self._number_of_vacancies = number_of_vacancies

    @abstractmethod
    def search_vacancies(self, job_title: str) -> list:
        """
        Метод для поиска вакансий.

        :param job_title: Заголовок вакансии.
        :return: Список найденных вакансий.
        """
        pass


class HeadHunterAPI(API):
    """Класс для запроса вакансий на HeadHunter API"""

    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """
        Инициализация класса HeadHunterAPI.

        :param url: URL для запросов к HeadHunter API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str) -> list:
        """
        Поиск вакансий на HeadHunter API.

        :param job_title: Заголовок вакансии для поиска.
        :return: Список найденных вакансий.
        """
        params = {
            'text': job_title,
            'per_page': self._number_of_vacancies,
            'only_with_salary': True
        }

        response = requests.get(url=self._base_url, params=params)
        response_json = response.json()

        return response_json.get("items", [])


class SuperJobAPI(API):
    """Класс запроса вакансий на SuperJob API"""
    url: str = "https://api.superjob.ru/2.0"

    def __init__(self, url: str = url):
        """
        Инициализация класса SuperJobAPI.

        :param url: URL для запросов к SuperJob API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str) -> list:
        """
        Поиск вакансий на SuperJob API.

        :param job_title: Заголовок вакансии для поиска.
        :return: Список найденных вакансий.
        """
        url = f"{self._base_url}/vacancies/"
        headers = {
            "X-Api-App-Id": os.getenv("API_SUPERJOB_KEY")
        }
        params = {
            "keywords": [[1, job_title]],
            "count": self._number_of_vacancies,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data.get("objects", [])
