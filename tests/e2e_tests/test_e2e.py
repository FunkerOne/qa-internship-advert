from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from framework.allure.allure import AllureParentSuite, AllureSuite, AllureTag
from framework.assertions.advertisements import (
    assert_get_advertisement_response,
    assert_get_advertisements_response,
    assert_get_statistics_response,
)
from framework.assertions.base import assert_status_code
from framework.assertions.schema import validate_json_schema
from framework.clients.advertisements.advertisements_client import AdvertisementsClient
from framework.fixtures.advertisements import AdvertisementsFixture
from framework.models.advertisements.advertisements_schema import (
    GetAdvertisementResponseSchema,
    GetAdvertisementsResponseSchema,
    GetStatisticsResponseSchema,
)
from framework.models.errors.errors_schema import NotFoundResponseSchema


@pytest.mark.e2e
@pytest.mark.regression
@allure.tag(AllureTag.E2E, AllureTag.POSITIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestE2EAdvertisement:
    @allure.tag(AllureTag.E2E)
    @allure.severity(Severity.NORMAL)
    @allure.title("Создание объявления -> получение -> получение всех -> получение статистики")
    def test_e2e_advertisement(
        self,
        get_advertisements_client: AdvertisementsClient,
        function_advertisement: AdvertisementsFixture,
    ) -> None:
        response = get_advertisements_client.get_advertisement_api(advertisement_id=function_advertisement.uuid)
        resp_data = GetAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_advertisement_response(resp_data, [function_advertisement.request])

        validate_json_schema(response.json(), resp_data.model_json_schema())

        get_adverts_response = get_advertisements_client.get_advertisements_api(
            seller_id=function_advertisement.seller_id
        )
        get_adverts_resp_data = GetAdvertisementsResponseSchema.model_validate_json(get_adverts_response.text)

        assert_status_code(get_adverts_response.status_code, HTTPStatus.OK)
        assert_get_advertisements_response(get_adverts_resp_data, [function_advertisement.request])

        validate_json_schema(get_adverts_response.json(), get_adverts_resp_data.model_json_schema())

        get_stats_response = get_advertisements_client.get_statistic_api(advertisement_id=function_advertisement.uuid)
        get_stats_resp_data = GetStatisticsResponseSchema.model_validate_json(get_stats_response.text)

        assert_status_code(get_stats_response.status_code, HTTPStatus.OK)
        assert_get_statistics_response(get_stats_resp_data, [function_advertisement.request])

        validate_json_schema(get_stats_response.json(), get_stats_resp_data.model_json_schema())

        get_advertisements_client.delete_advertisement_api(advertisement_id=function_advertisement.uuid)

        non_existent_advert_response = get_advertisements_client.get_advertisement_api(
            advertisement_id=function_advertisement.uuid
        )
        non_existent_advert_resp_data = NotFoundResponseSchema.model_validate_json(non_existent_advert_response.text)

        assert_status_code(non_existent_advert_response.status_code, HTTPStatus.NOT_FOUND)

        validate_json_schema(non_existent_advert_response.json(), non_existent_advert_resp_data.model_json_schema())
