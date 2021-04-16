from delivery.builders.filter_builder import Filter
import pytest

import config
from delivery.client import DeliveryClient

reason="avoid calling live API in automated tests."

# ITEMS
# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_items_pass(delivery_client):
    r = delivery_client.get_content_items()
    assert  r.api_response.ok == True
    assert r.items is not None
    assert r.count > 0

# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_items_with_filters_pass(delivery_client):
    r = delivery_client.get_content_items(
        Filter("system.type", "[eq]", "coffee"),
        Filter("elements.price", "[range]", "10.5,50"),
        Filter("","depth", 6)
    )
    assert r.api_response.ok == True
    assert r.items[0].codename is not None
    assert r.count > 0

# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_item_pass(delivery_client):
    r = delivery_client.get_content_item("on_roasts")
    assert r.api_response.ok == True
    assert r.codename


# TYPES
# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_type_pass(delivery_client):
    r = delivery_client.get_content_type("article")
    assert r.api_response.ok == True
    assert r.codename

# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_types_pass(delivery_client):
    r = delivery_client.get_content_types()
    assert r.api_response.ok == True
    assert r.count > 0

# TAXONOMIES
# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_taxonomies_pass(delivery_client):
    r = delivery_client.get_taxonomies()
    assert r.api_response.ok == True
    assert r.count > 0

# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_taxonomy_pass(delivery_client):
    r = delivery_client.get_taxonomy("personas")
    assert r.api_response.ok == True
    assert r.codename

# LANGUAGES
# @pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_languages_pass(delivery_client):
    r = delivery_client.get_languages()
    assert r.api_response.ok == True
    assert len(r.languages) > 0
    # assert r.count > 0

# @pytest.mark.skip(reason)
#@pytest.mark.usefixtures("delivery_client")
def test_performance():
    delivery_client = DeliveryClient(config.project_id, options=config.delivery_options)
    # delivery_client = DeliveryClient(config.project_id)
    # a = delivery_client.get_languages()
    # b = delivery_client.get_content_items()
    # c = delivery_client.get_content_item("on_roasts")
    d = delivery_client.get_content_items(
        Filter("system.type", "[eq]", "coffee"),
        Filter("elements.price", "[range]", "10.5,50"),
        Filter("","depth", 6),
        Filter("","order","system.name[desc]"),
        Filter("elements.price","[neq]","blah")
    )
    # e = delivery_client.get_content_type("article")
    # f = delivery_client.get_content_types()
    # g = delivery_client.get_taxonomies()
    # h = delivery_client.get_taxonomy("personas")