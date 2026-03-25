import allure

from framework.assertions.base import assert_not_empty, assert_equal, assert_length
from framework.models.advertisements.advertisements_schema import (
    CreateAdvertisementResponseSchema,
    AdvertisementSchema,
    GetAdvertisementResponseSchema,
    CreateAdvertisementRequestSchema,
    GetAdvertisementsResponseSchema,
    StatisticsSchema,
    GetStatisticsResponseSchema,
)
from framework.utils.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")


@allure.step("Проверка ответа создания объявления")
def assert_create_advertisement_response(response: CreateAdvertisementResponseSchema):
    """
    Проверяет корректность ответа на создание объявления.

    :param response: Ответ API со статусом.
    :raises AssertionError: Если значение поля не совпадает.
    """
    logger.info("Проверка ответа создания объявления")

    assert_not_empty(response.status, "status")


@allure.step("Проверка объявления")
def assert_advertisement(actual: AdvertisementSchema, expected: CreateAdvertisementRequestSchema) -> None:
    """
    Проверяет, что фактические данные объявления соответствуют ожидаемым.

    :param actual: Фактические данные объявления.
    :param expected: Ожидаемые данные объявления.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Проверка объявления")

    assert_not_empty(actual.id, "id")
    assert_equal(actual.seller_id, expected.seller_id, "seller_id")
    assert_equal(actual.name, expected.name, "name")
    assert_equal(actual.price, expected.price, "price")
    assert_statistics(actual.statistics, expected)
    assert_not_empty(actual.id, "created_at")


@allure.step("Проверка ответа на получение объявления")
def assert_get_advertisement_response(
    get_advertisement_response: GetAdvertisementResponseSchema,
    create_advertisement_requests: list[CreateAdvertisementRequestSchema],
) -> None:
    """
    Проверяет, что ответ на получение объявления соответствует запросу на его создание.

    :param get_advertisement_response: Ответ API при запросе данных объявления.
    :param create_advertisement_requests: Запрос на создании объявления.
    :raises AssertionError: Если данные объявления не совпадают.
    """
    logger.info("Проверка ответа на получение объявления")

    assert_length(get_advertisement_response.root, create_advertisement_requests, "root")

    for idx, create_advertisement_request in enumerate(create_advertisement_requests):
        assert_advertisement(get_advertisement_response.root[idx], create_advertisement_request)


@allure.step("Проверка ответа на получение объявлений")
def assert_get_advertisements_response(
    get_advertisements_response: GetAdvertisementsResponseSchema,
    create_advertisement_requests: list[CreateAdvertisementRequestSchema],
) -> None:
    """
    Проверяет, что ответ на получение объявления соответствует запросу на его создание.

    :param get_advertisements_response: Ответ API при запросе данных объявлений.
    :param create_advertisement_requests: Запрос на создании объявления.
    :raises AssertionError: Если данные объявления не совпадают.
    """
    logger.info("Проверка ответа на получение объявления")

    assert_length(get_advertisements_response.root, create_advertisement_requests, "root")

    for idx, create_advertisement_request in enumerate(create_advertisement_requests):
        assert_advertisement(get_advertisements_response.root[idx], create_advertisement_request)


@allure.step("Проверка статистики")
def assert_statistics(actual: StatisticsSchema, expected: CreateAdvertisementRequestSchema) -> None:
    """
    Проверяет, что фактические данные статистики соответствуют ожидаемым.

    :param actual: Фактические данные статистики.
    :param expected: Ожидаемые данные статистики.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Проверка статистики")

    assert_equal(actual.likes, expected.statistics.likes, "likes")
    assert_equal(actual.view_count, expected.statistics.view_count, "view_count")
    assert_equal(actual.contacts, expected.statistics.contacts, "contacts")


@allure.step("Проверка ответа на получение статистики")
def assert_get_statistics_response(
    get_statistics_response: GetStatisticsResponseSchema,
    create_advertisement_requests: list[CreateAdvertisementRequestSchema],
) -> None:
    """
    Проверяет, что ответ на получение статистики соответствует запросу на его создание.

    :param get_statistics_response: Ответ API при запросе данных статистики.
    :param create_advertisement_requests: Запрос на создании объявления.
    :raises AssertionError: Если данные статистики не совпадают.
    """
    logger.info("Проверка ответа на получение статистики")

    assert_length(get_statistics_response.root, create_advertisement_requests, "root")

    for idx, create_advertisement_request in enumerate(create_advertisement_requests):
        assert_statistics(get_statistics_response.root[idx], create_advertisement_request)
