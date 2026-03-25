from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from framework.allure.allure import AllureParentSuite, AllureSuite, AllureSubSuite, AllureTag
from framework.assertions.advertisements import assert_get_advertisement_response
from framework.assertions.base import assert_status_code
from framework.assertions.schema import validate_json_schema
from framework.clients.advertisements.advertisements_client import AdvertisementsClient
from framework.fixtures.advertisements import AdvertisementsFixture
from framework.models.advertisements.advertisements_schema import GetAdvertisementResponseSchema
from framework.models.errors.errors_schema import NotFoundResponseSchema, BadRequestResponseSchema


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.POSITIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestGetAdvertisement:
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение существующего объявления")
    def test_get_advertisement_existing(
        self,
        get_advertisements_client: AdvertisementsClient,
        function_advertisement: AdvertisementsFixture,
    ) -> None:
        response = get_advertisements_client.get_advertisement_api(advertisement_id=function_advertisement.uuid)
        resp_data = GetAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_advertisement_response(resp_data, [function_advertisement.request])

        validate_json_schema(response.json(), resp_data.model_json_schema())

        get_advertisements_client.delete_advertisement_api(advertisement_id=function_advertisement.uuid)


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.NEGATIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestNegativeGetAdvertisement:
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @pytest.mark.xfail(reason="Известный баг")
    @allure.title("Получение несуществующего объявления")
    def test_get_advertisement_non_existent(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisement_api(
            advertisement_id="550e8400-e29b-41d4-a716-446655440000"
        )
        resp_data = NotFoundResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение объявления c невалидным uuid")
    def test_get_advertisement_invalid_uuid(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisement_api(advertisement_id="erfdfgrtf34dbgffe")
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @pytest.mark.xfail(reason="Известный баг")
    @allure.title("Получение объявления с uuid = 'Пустой ввод'")
    def test_get_advertisement_empty_uuid(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisement_api(advertisement_id="")
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        validate_json_schema(response.json(), resp_data.model_json_schema())
