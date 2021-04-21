import pytest
from delivery.client import DeliveryClient
from delivery.builders.filter_builder import Filter, FilterBuilder
from delivery.builders.url_builder import UrlBuilder

PROTOCOL = "https://"
DELIVERY_DOMAIN = "deliver.kontent.ai/"
PREVIEW_DOMAIN = "preview-deliver.kontent.ai/"
TEST_PARAMETERS = "?system.codename[eq]=on_roasts&elements.personas[contains]=barista&depth=6"

filters = [
    Filter("system.codename", "[eq]", "on_roasts"),
    Filter("elements.personas", "[contains]", "barista"),
    Filter("", "depth", 6)
]

query_string = FilterBuilder().build_return_url(filters)

client =  DeliveryClient("test_project_id")

delivery_options = {
                        "preview":True, 
                        "preview_api_key":"test_key"
                    }
preview_client =  DeliveryClient("test_project_id", options=delivery_options)

    
@pytest.mark.parametrize("client, endpoint, query_string, result",
                            [(
                                client,
                                "/items",
                                "",
                                f"{PROTOCOL}{DELIVERY_DOMAIN}test_project_id/items",
                            ),
                            (
                                client,
                                "/items",
                                query_string,
                                f"{PROTOCOL}{DELIVERY_DOMAIN}test_project_id/items{TEST_PARAMETERS}",
                            )])
def test_build_delivery_url(client, endpoint, query_string, result):
    assert UrlBuilder().build_url(client, endpoint, query_string) == result

@pytest.mark.parametrize("client, endpoint, query_string, result",
                            [(
                                preview_client,
                                "/items",
                                "",
                                f"{PROTOCOL}{PREVIEW_DOMAIN}test_project_id/items",
                            ),
                            (
                                preview_client,
                                "/items",
                                query_string,
                                f"{PROTOCOL}{PREVIEW_DOMAIN}test_project_id/items{TEST_PARAMETERS}",
                            )])
def test_build_preview_url(client, endpoint, query_string, result):
    assert UrlBuilder().build_url(client, endpoint, query_string) == result