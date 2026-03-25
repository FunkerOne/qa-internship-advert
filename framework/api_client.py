import allure

from typing import Any
from httpx import Client, URL, Response


class APIClient:
    def __init__(self, client: Client):
        """
        Базовый API клиент, принимающий объект httpx.Client.

        :param client: экземпляр httpx.Client для выполнения HTTP-запросов
        """
        self.client = client

    @allure.step("Отправить GET запрос на {url}")
    def get(self, url: URL | str) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url)

    @allure.step("Отправить POST запрос на {url}")
    def post(
        self,
        url: URL | str,
        json: Any | None = None,
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url, json=json)

    @allure.step("Отправить DELETE запрос на {url}")
    def delete(self, url: URL | str) -> Response:
        """
        Выполняет DELETE-запрос (удаление данных).

        :param url: URL-адрес эндпоинта.
        :return: Объект Response с данными ответа.
        """
        return self.client.delete(url)
