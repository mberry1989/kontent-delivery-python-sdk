import pytest
import config
from delivery.client import DeliveryClient
from samples.custom_link_resolver import CustomLinkResolver


@pytest.fixture(scope="module")
def delivery_client():
    return DeliveryClient(config.project_id)

@pytest.fixture(scope="module")
def preview_delivery_client():
    return DeliveryClient(config.project_id, options=config.delivery_options)

@pytest.fixture(scope="module")
def delivery_client_with_resolvers():
    client = DeliveryClient(config.project_id)
    client.custom_link_resolver = CustomLinkResolver()
    return client