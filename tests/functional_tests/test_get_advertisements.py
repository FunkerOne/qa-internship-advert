from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from framework.allure.allure import AllureParentSuite, AllureSuite, AllureSubSuite, AllureTag
from framework.assertions.advertisements import assert_get_advertisements_response
from framework.assertions.base import assert_status_code
from framework.assertions.schema import validate_json_schema
from framework.clients.advertisements.advertisements_client import AdvertisementsClient
from framework.fixtures.advertisements import AdvertisementsFixture
from framework.models.advertisements.advertisements_schema import GetAdvertisementsResponseSchema
from framework.models.errors.errors_schema import NotFoundResponseSchema, BadRequestResponseSchema


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.POSITIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestGetAdvertisements:
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @allure.title("Получение существующих объявлений")
    def test_get_advertisements_existing(
        self,
        get_advertisements_client: AdvertisementsClient,
        function_advertisement: AdvertisementsFixture,
    ) -> None:
        response = get_advertisements_client.get_advertisements_api(seller_id=function_advertisement.seller_id)
        resp_data = GetAdvertisementsResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_advertisements_response(resp_data, [function_advertisement.request])

        validate_json_schema(response.json(), resp_data.model_json_schema())

        get_advertisements_client.delete_advertisement_api(advertisement_id=function_advertisement.uuid)


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.NEGATIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestNegativeGetAdvertisements:
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @pytest.mark.xfail(reason="Известный баг")
    @allure.title("Получение объявлений по несуществующему seller_id")
    def test_get_advertisements_non_existent_seller_id(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisements_api(seller_id=-500)
        resp_data = NotFoundResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @pytest.mark.xfail(reason="Известный баг")
    @allure.title("Получение объявлений по невалидному seller_id")
    def test_get_advertisement_invalid_seller_id(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisements_api(seller_id="ddfgfghjgydf#@$")
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @pytest.mark.xfail(reason="Известный баг")
    @allure.title("Получение объявлений с seller_id = 'Пустой ввод'")
    def test_get_advertisement_empty_seller_id(
        self,
        get_advertisements_client: AdvertisementsClient,
    ) -> None:
        response = get_advertisements_client.get_advertisements_api(seller_id="")
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        validate_json_schema(response.json(), resp_data.model_json_schema())
