import pytest
import config
from delivery.client import DeliveryClient


@pytest.fixture(scope="module")
def delivery_client():
    return DeliveryClient(config.project_id)

def preview_delivery_client():
    return DeliveryClient(config.project_id, options=config.delivery_options)