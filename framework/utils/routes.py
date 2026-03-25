from enum import StrEnum


class APIRoutes(StrEnum):
    """
    Класс описывает основные URI сервиса.
    """

    ITEM_1 = "/api/1/item"
    STATISTIC_1 = "/api/1/statistic"
    ROOT_1 = "/api/1"

    ITEM_2 = "/api/2/item"
    STATISTIC_2 = "/api/2/statistic"
