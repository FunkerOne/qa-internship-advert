from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from framework.allure.allure import AllureParentSuite, AllureSuite, AllureSubSuite, AllureTag
from framework.assertions.advertisements import (
    assert_create_advertisement_response,
    assert_get_advertisement_response,
)
from framework.assertions.base import assert_status_code
from framework.assertions.schema import validate_json_schema
from framework.clients.advertisements.advertisements_client import AdvertisementsClient
from framework.models.advertisements.advertisements_schema import (
    CreateAdvertisementRequestSchema,
    CreateAdvertisementResponseSchema,
    GetAdvertisementResponseSchema,
    StatisticsSchema,
)
from framework.models.errors.errors_schema import BadRequestResponseSchema
from framework.utils.faker import fake


test_data_title = (
    ("кирилических букв", "Телевизор Закат"),
    ("латинских букв", "PearBook Lite"),
    ("пробела в начале", " Телефон"),
    ("пробела в конце", "Телефон "),
    ("точки в конце", "Приставка."),
)


test_data_price = (
    ("цифры", 1),
    ("числа миллион", 1_000_000),
)

test_data_statistics = (pytest.param(0, marks=pytest.mark.xfail(reason="Известный баг")), 1, 10_000)


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.POSITIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestCreateAdvertisement:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание двух одинаковых объявления")
    def test_create_two_identical_advertisement(self, get_advertisements_client: AdvertisementsClient) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name="Моё новое объявление",
            price=5_000,
            statistics=StatisticsSchema(likes=5, viewCount=5, contacts=5),
        )
        for i in range(1):
            response = get_advertisements_client.create_advertisement_api(request=request)
            resp_data = CreateAdvertisementResponseSchema.model_validate_json(response.text)

            assert_status_code(response.status_code, HTTPStatus.OK)
            assert_create_advertisement_response(resp_data)

            validate_json_schema(response.json(), resp_data.model_json_schema())

            resp_get_advert = get_advertisements_client.get_advertisement_api(advertisement_id=resp_data.status[-36:])
            get_advert_resp_data = GetAdvertisementResponseSchema.model_validate_json(resp_get_advert.text)
            assert_get_advertisement_response(get_advert_resp_data, [request])

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, ad_title", test_data_title)
    @allure.title("Создание объявления c названием, состоящим из {details}: '{ad_title}'")
    def test_create_advertisement_with_diff_titles(
        self, details, ad_title, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=ad_title,
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = CreateAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_advertisement_response(resp_data)

        validate_json_schema(response.json(), resp_data.model_json_schema())

        resp_get_advert = get_advertisements_client.get_advertisement_api(advertisement_id=resp_data.status[-36:])
        get_advert_resp_data = GetAdvertisementResponseSchema.model_validate_json(resp_get_advert.text)

        assert_get_advertisement_response(get_advert_resp_data, [request])

        get_advertisements_client.delete_advertisement_api(advertisement_id=resp_data.status[-36:])

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, price", test_data_price)
    @allure.title("Создание объявления c ценой, состоящей из {details}: '{price}'")
    def test_create_advertisement_with_diff_prices(
        self, details, price, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=price,
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = CreateAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_advertisement_response(resp_data)

        validate_json_schema(response.json(), resp_data.model_json_schema())

        resp_get_advert = get_advertisements_client.get_advertisement_api(advertisement_id=resp_data.status[-36:])
        get_advert_resp_data = GetAdvertisementResponseSchema.model_validate_json(resp_get_advert.text)

        assert_get_advertisement_response(get_advert_resp_data, [request])

        get_advertisements_client.delete_advertisement_api(advertisement_id=resp_data.status[-36:])

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("stat_name", ["likes", "view_count", "contacts"])
    @pytest.mark.parametrize("data", test_data_statistics)
    @allure.title("Создание объявления cо статистикой поля {stat_name}, состоящей из '{data}'")
    def test_create_advertisement_with_diff_stats(
        self, stat_name, data, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=data, viewCount=data, contacts=data),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = CreateAdvertisementResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_advertisement_response(resp_data)

        validate_json_schema(response.json(), resp_data.model_json_schema())

        resp_get_advert = get_advertisements_client.get_advertisement_api(advertisement_id=resp_data.status[-36:])
        get_advert_resp_data = GetAdvertisementResponseSchema.model_validate_json(resp_get_advert.text)

        assert_get_advertisement_response(get_advert_resp_data, [request])

        get_advertisements_client.delete_advertisement_api(advertisement_id=resp_data.status[-36:])


test_invalid_seller_id = (
    ("спецсимволов", "!@!#$@$#%#$@%"),
    ("латинских букв", "John"),
    ("пустой строки", ""),
    ("значения в типе данных string", "999"),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", [1000]),
    ("значения в типе данных null", None),
)

test_invalid_data_title = (
    pytest.param("одной кириллической буквы", "А", marks=pytest.mark.xfail(reason="Известный баг")),
    pytest.param("спецсимволов", "!@!#$@$#%#$@%", marks=pytest.mark.xfail(reason="Известный баг")),
    pytest.param("арабской вязи", "سلسلة اختبار", marks=pytest.mark.xfail(reason="Известный баг")),
    ("пустого ввода", ""),
    ("значения в типе данных number", 123456),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", ["Чайник 1000W"]),
    ("значения в типе данных null", None),
    pytest.param("SQL инъекции", "' OR 1=1 --", marks=pytest.mark.xfail(reason="Известный баг")),
)

test_invalid_data_price = (
    ("очень большого числа", 10000000000000000000000000),
    pytest.param("отрицательного числа", -1000, marks=pytest.mark.xfail(reason="Известный баг")),
    ("вещественного числа", 3399.99),
    ("отрицательного вещественного числа", -1549.49),
    ("спецсимволов", "%:№;$#%#$@%"),
    ("японских иероглифов", "東京は美しいです"),
    ("пустой строки", ""),
    ("значения в типе данных string", "999"),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", [1000]),
    ("значения в типе данных null", None),
    ("SQL инъекции", "' OR 1=1 --"),
)

test_invalid_stats_likes = (
    ("очень большого числа", 10000000000000000000000000),
    pytest.param("отрицательного числа", -1000, marks=pytest.mark.xfail(reason="Известный баг")),
    ("вещественного числа", 3399.99),
    ("отрицательного вещественного числа", -1549.49),
    ("спецсимволов", "%:№;$#%#$@%"),
    ("японских иероглифов", "東京は美しいです"),
    ("пустой строки", ""),
    ("значения в типе данных string", "999"),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", [1000]),
    ("значения в типе данных null", None),
    ("SQL инъекции", "' OR 1=1 --"),
)

test_invalid_stats_view_count = (
    ("очень большого числа", 10000000000000000000000000),
    pytest.param("отрицательного числа", -1000, marks=pytest.mark.xfail(reason="Известный баг")),
    ("вещественного числа", 3399.99),
    ("отрицательного вещественного числа", -1549.49),
    ("спецсимволов", "%:№;$#%#$@%"),
    ("японских иероглифов", "東京は美しいです"),
    ("пустой строки", ""),
    ("значения в типе данных string", "999"),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", [1000]),
    ("значения в типе данных null", None),
    ("SQL инъекции", "' OR 1=1 --"),
)

test_invalid_stats_contacts = (
    ("очень большого числа", 10000000000000000000000000),
    pytest.param("отрицательного числа", -1000, marks=pytest.mark.xfail(reason="Известный баг")),
    ("вещественного числа", 3399.99),
    ("отрицательного вещественного числа", -1549.49),
    ("спецсимволов", "%:№;$#%#$@%"),
    ("японских иероглифов", "東京は美しいです"),
    ("пустой строки", ""),
    ("значения в типе данных string", "999"),
    ("значения в типе данных boolean", True),
    ("значения в типе данных array", [1000]),
    ("значения в типе данных null", None),
    ("SQL инъекции", "' OR 1=1 --"),
)


@pytest.mark.functional
@pytest.mark.regression
@allure.tag(AllureTag.FUNCTION, AllureTag.NEGATIVE, AllureTag.REGRESSION)
@allure.parent_suite(AllureParentSuite.ADVERTISEMENTS)
@allure.suite(AllureSuite.ADVERTISEMENTS)
class TestNegativeCreateAdvertisement:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_ad_seller_id", test_invalid_seller_id)
    @allure.title("Создание объявления c идентификатором продавца, состоящим из {details}: '{invalid_ad_seller_id}'")
    def test_create_advertisement_with_invalid_seller_id(
        self, details, invalid_ad_seller_id, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=invalid_ad_seller_id,
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_ad_title", test_invalid_data_title)
    @allure.title("Создание объявления c названием, состоящим из {details}: '{invalid_ad_title}'")
    def test_create_advertisement_with_invalid_titles(
        self, details, invalid_ad_title, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=invalid_ad_title,
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без поля name")
    def test_create_advertisement_without_name_field(self, get_advertisements_client: AdvertisementsClient) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.name
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_ad_price", test_invalid_data_price)
    @allure.title("Создание объявления c ценой, состоящей из {details}: '{invalid_ad_price}'")
    def test_create_advertisement_with_invalid_prices(
        self, details, invalid_ad_price, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=invalid_ad_price,
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без поля price")
    def test_create_advertisement_without_price_field(self, get_advertisements_client: AdvertisementsClient) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.price
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_stats_likes", test_invalid_stats_likes)
    @allure.title("Создание объявления cо статистикой поля likes, состоящим из {details}: '{invalid_stats_likes}'")
    def test_create_advertisement_with_invalid_stats_likes_field(
        self, details, invalid_stats_likes, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(
                likes=invalid_stats_likes, viewCount=fake.view_count(), contacts=fake.contacts()
            ),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без поля статистики likes")
    def test_create_advertisement_without_stats_likes_field(
        self, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.statistics.likes
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_stats_view_count", test_invalid_stats_view_count)
    @allure.title(
        "Создание объявления cо статистикой поля view_count, состоящим из {details}: '{invalid_stats_view_count}'"
    )
    def test_create_advertisement_with_invalid_stats_view_count_field(
        self, details, invalid_stats_view_count, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(
                likes=fake.likes(), viewCount=invalid_stats_view_count, contacts=fake.contacts()
            ),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без поля статистики view_count")
    def test_create_advertisement_without_stats_view_count_field(
        self, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.statistics.view_count
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("details, invalid_stats_contacts", test_invalid_stats_contacts)
    @allure.title(
        "Создание объявления cо статистикой поля contacts, состоящим из {details}: '{invalid_stats_contacts}'"
    )
    def test_create_advertisement_with_invalid_stats_contacts_field(
        self, details, invalid_stats_contacts, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(
                likes=fake.likes(), viewCount=fake.view_count(), contacts=invalid_stats_contacts
            ),
        )
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без поля статистики contacts")
    def test_create_advertisement_without_stats_contacts_field(
        self, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.statistics.contacts
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание объявления без объекта statistics")
    def test_create_advertisement_without_statistics_object(
        self, get_advertisements_client: AdvertisementsClient
    ) -> None:
        request = CreateAdvertisementRequestSchema(
            sellerID=fake.seller_id(),
            name=f"Моё объявление {fake.integer()!s}",
            price=fake.price(),
            statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
        )
        del request.statistics
        response = get_advertisements_client.create_advertisement_api(request=request)
        resp_data = BadRequestResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        validate_json_schema(response.json(), resp_data.model_json_schema())
