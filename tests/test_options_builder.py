from kontent_delivery.builders.options_builder import DeliveryOptionsBuilder
from kontent_delivery.client import DeliveryClient
import pytest

client = DeliveryClient("test_project_id")


def test_preview_with_api_key():
    delivery_options = {"options": {
                        "preview": True,
                        "preview_api_key": "test_key"}
                        }
    assert DeliveryOptionsBuilder.build_client_options(client, options=delivery_options) != type(Exception)


def test_preview_without_api_key_exception():
    with pytest.raises(Exception):
        delivery_options = {"options": {
                            "preview": True}
                            }
        DeliveryOptionsBuilder.build_client_options(client, options=delivery_options)


def test_secured_with_api_key():
    delivery_options = {"options": {
                        "secured": True,
                        "secured_api_key": "test_key"}
                        }
    assert DeliveryOptionsBuilder.build_client_options(client, options=delivery_options) != type(Exception)


def test_secured_without_api_key_exception():
    with pytest.raises(Exception):
        delivery_options = {"options": {
                            "secured": True}
                            }
        DeliveryOptionsBuilder.build_client_options(client, options=delivery_options)
