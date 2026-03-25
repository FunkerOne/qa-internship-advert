import pytest

from pydantic import BaseModel

from framework.clients.advertisements.advertisements_client import (
    AdvertisementsClient,
    advertisements_client,
)
from framework.models.advertisements.advertisements_schema import (
    CreateAdvertisementRequestSchema,
    CreateAdvertisementResponseSchema,
    StatisticsSchema,
)
from framework.utils.faker import fake


class AdvertisementsFixture(BaseModel):
    request: CreateAdvertisementRequestSchema
    response: CreateAdvertisementResponseSchema

    @property
    def uuid(self):
        uuid = self.response.status[-36:]
        return uuid

    @property
    def seller_id(self):
        return self.request.seller_id


@pytest.fixture(scope="session")
def get_advertisements_client() -> AdvertisementsClient:
    return advertisements_client()


@pytest.fixture
def function_advertisement(
    get_advertisements_client: AdvertisementsClient,
) -> AdvertisementsFixture:
    request = CreateAdvertisementRequestSchema(
        sellerID=fake.seller_id(),
        name=f"Моё объявление {fake.integer()!s}",
        price=fake.price(),
        statistics=StatisticsSchema(likes=fake.likes(), viewCount=fake.view_count(), contacts=fake.contacts()),
    )
    response = get_advertisements_client.create_advertisement(request=request)
    return AdvertisementsFixture(request=request, response=response)
