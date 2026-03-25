import allure

from httpx import Response

from framework.http_builder import get_http_client
from framework.utils.routes import APIRoutes
from framework.api_client import APIClient

from framework.models.advertisements.advertisements_schema import (
    CreateAdvertisementRequestSchema,
    CreateAdvertisementResponseSchema,
)


class AdvertisementsClient(APIClient):
    """
    Клиент для работы с /api/1/item/
    """

    @allure.step("Сохранить (создать) объявление")
    def create_advertisement_api(self, request: CreateAdvertisementRequestSchema) -> Response:
        """
        Метод создания (сохранения) объявления.

        :param request: Словарь с sellerId, name, price, statistics.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(url=APIRoutes.ITEM_1, json=request.model_dump(by_alias=True))

    @allure.step("Получить объявление по идентификатору {advertisement_id}")
    def get_advertisement_api(self, advertisement_id: str) -> Response:
        """
        Метод получения объявления.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(url=f"{APIRoutes.ITEM_1}/{advertisement_id}")

    @allure.step("Получить все объявления по идентификатору продавца {seller_id}")
    def get_advertisements_api(self, seller_id: int | str) -> Response:
        """
        Метод получения объявлений.

        :param seller_id: Идентификатор продавца.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(url=f"{APIRoutes.ROOT_1}/{seller_id}/item")

    @allure.step("Получить статистику по объявлению с идентификатором {advertisement_id}")
    def get_statistic_api(self, advertisement_id: str) -> Response:
        """
        Метод получения статистики по объявлению.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(url=f"{APIRoutes.STATISTIC_1}/{advertisement_id}")

    @allure.step("Удалить объявление по идентификатору {advertisement_id}")
    def delete_advertisement_api(self, advertisement_id: str) -> Response:
        """
        Метод удаления объявления.

        :param advertisement_id: Идентификатор объявления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(url=f"{APIRoutes.ITEM_2}/{advertisement_id}")

    def create_advertisement[T, U](
        self, request: CreateAdvertisementRequestSchema[T, U]
    ) -> CreateAdvertisementResponseSchema:
        response = self.create_advertisement_api(request=request)
        return CreateAdvertisementResponseSchema.model_validate_json(response.text)


def advertisements_client() -> AdvertisementsClient:
    """
    Функция создаёт экземпляр AdvertisementsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AdvertisementsClient.
    """
    return AdvertisementsClient(client=get_http_client())
