from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from framework.allure.allure import AllureParentSuite, AllureSuite, AllureSubSuite, AllureTag
from framework.assertions.base import assert_status_code
from framework.assertions.schema import validate_json_schema
from framework.clients.advertisements.advertisements_client import (
    advertisements_client,
    AdvertisementsClient,
)
from framework.fixtures.advertisements import AdvertisementsFixture
from framework.models.advertisements.advertisements_schema import (
    CreateAdvertisementRequestSchema,
    StatisticsSchema,
    CreateAdvertisementResponseSchema,
    GetAdvertisementResponseSchema,
    GetAdvertisementsResponseSchema,
    GetStatisticsResponseSchema,
)
from framework.utils.faker import fake


@pytest.mark.smoke
@allure.tag(AllureTag.SMOKE)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestAdvertisements:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создать объявление")
    def test_create_advertisement(self, get_advertisements_client: AdvertisementsClient) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = CreateAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), resp_data.model_json_schema())
        get_advertisements_client.delete_advertisement_api(advertisement_id=resp_data.status[-36:])

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получить объявление")
    def test_get_advertisement(
        self,
        function_advertisement: AdvertisementsFixture,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = advertisements_client().get_advertisement_api(advertisement_id=function_advertisement.uuid)
        resp_data = GetAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), resp_data.model_json_schema())
        get_advertisements_client.delete_advertisement_api(function_advertisement.uuid)

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @allure.title("Получить объявления")
    def test_get_advertisements(
        self,
        function_advertisement: AdvertisementsFixture,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = advertisements_client().get_advertisements_api(seller_id=function_advertisement.seller_id)
        resp_data = GetAdvertisementsResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), resp_data.model_json_schema())
        get_advertisements_client.delete_advertisement_api(function_advertisement.uuid)

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получить статистику по объявлению")
    def test_get_statistics(
        self,
        function_advertisement: AdvertisementsFixture,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = advertisements_client().get_statistic_api(advertisement_id=function_advertisement.uuid)
        resp_data = GetStatisticsResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), resp_data.model_json_schema())
        get_advertisements_client.delete_advertisement_api(function_advertisement.uuid)
