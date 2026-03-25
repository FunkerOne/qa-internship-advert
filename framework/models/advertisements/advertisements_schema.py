from pydantic import BaseModel, Field, RootModel, ConfigDict


class StatisticsSchema[T](BaseModel):
    """
    Описание структуры статистики.
    """

    model_config = ConfigDict(populate_by_name=True)

    likes: int | T
    view_count: int | T = Field(alias="viewCount")
    contacts: int | T


class CreateAdvertisementRequestSchema[T, U](BaseModel):
    """
    Описание структуры запроса на создание объявления.
    """

    model_config = ConfigDict(populate_by_name=True)

    seller_id: int | T = Field(alias="sellerID")  # Баг ли в названии поля?
    name: str | U
    price: int | T
    statistics: StatisticsSchema[T]


class CreateAdvertisementResponseSchema(BaseModel):
    """
    Описание структуры ответа создания объявления.
    """

    status: str


class AdvertisementSchema(BaseModel):
    """
    Описание структуры объявления.
    """

    id: str
    seller_id: int = Field(alias="sellerId")
    name: str
    price: int
    statistics: StatisticsSchema
    created_at: str = Field(alias="createdAt")


class GetAdvertisementResponseSchema(RootModel):
    """
    Описание структуры ответа получения объявления.
    """

    root: list[AdvertisementSchema]


class GetAdvertisementsResponseSchema(RootModel):
    """
    Описание структуры ответа получения всех объявлений пользователя.
    """

    root: list[AdvertisementSchema]


class GetStatisticsResponseSchema(RootModel):
    """
    Описание структуры ответа получения статистики по объявлению.
    """

    root: list[StatisticsSchema]
