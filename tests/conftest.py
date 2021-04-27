import pytest
import tests.conftest_keys as test_config
from kontent_delivery.client import DeliveryClient
from samples.custom_link_resolver import CustomLinkResolver
from samples.custom_item_resolver import CustomItemResolver


@pytest.fixture(scope="module")
def delivery_client():
    return DeliveryClient(test_config.project_id)


@pytest.fixture(scope="module")
def delivery_client_with_options():
    return DeliveryClient(test_config.project_id, options=test_config.delivery_options)


@pytest.fixture(scope="module")
def delivery_client_with_resolvers():
    client = DeliveryClient(test_config.project_id)
    client.custom_link_resolver = CustomLinkResolver()
    client.custom_item_resolver = CustomItemResolver()
    return client
