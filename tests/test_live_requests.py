from delivery.builders.filter_builder import Filter
import pytest

reason="avoid calling live API in automated tests."

@pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_items_pass(delivery_client):
    r = delivery_client.get_content_items()
    assert  r.api_response.ok == True
    assert r.items is not None
    assert r.count > 0

@pytest.mark.skip(reason)
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

@pytest.mark.skip(reason)
@pytest.mark.usefixtures("delivery_client")
def test_get_content_item_pass(delivery_client):
    r = delivery_client.get_content_item("on_roasts")
    assert r.api_response.ok == True
    assert r.codename
