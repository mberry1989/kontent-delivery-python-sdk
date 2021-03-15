import pytest

@pytest.mark.skip(reason="avoid calling live API in automated tests.")
@pytest.mark.usefixtures("delivery_client")
def test_get_content_items_pass(delivery_client):
    response = delivery_client.get_content_items()
    assert  response.status_code == 200
    assert "items" in response.json()
