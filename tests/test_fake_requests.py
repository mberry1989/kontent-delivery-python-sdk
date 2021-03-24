import json
import pytest
from delivery.request_manager import RequestManager
from delivery.builders.filter_builder import Filter

# PATHS
@pytest.fixture
def items_path():
    return "tests/fixtures/items.json"

@pytest.fixture
def items_with_filters_path():
    return "tests/fixtures/items_with_filters.json"

@pytest.fixture
def single_item_path():
    return "tests/fixtures/on_roasts.json"

@pytest.fixture
def articles_path():
    return "tests/fixtures/articles_with_depth_6.json"

@pytest.fixture
def article_type_path():
    return "tests/fixtures/article_type.json"

@pytest.fixture
def types_path():
    return "tests/fixtures/types.json"


# RESPONSES
@pytest.fixture
def mock_items_response(monkeypatch, items_path):
    def mock_get(*args):
        return MockResponse(items_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)

@pytest.fixture
def mock_items_with_filters_response(monkeypatch, items_with_filters_path):
    def mock_get(*args):
        return MockResponse(items_with_filters_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)

@pytest.fixture
def mock_item_response(monkeypatch, single_item_path):
    def mock_get(*args):
        return MockResponse(single_item_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)

@pytest.fixture
def mock_articles_response(monkeypatch, articles_path):
    def mock_get(*args):
        return MockResponse(articles_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)

@pytest.fixture
def mock_article_type_response(monkeypatch, article_type_path):
    def mock_get(*args):
        return MockResponse(article_type_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)

@pytest.fixture
def mock_types_response(monkeypatch, types_path):
    def mock_get(*args):
        return MockResponse(types_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)


# MOCK
class MockResponse:
    def __init__(self, path):
        self.ok = True
        self.path = path

    def json(self):
        with open(self.path) as f:
            data = json.load(f)
        return data
        
        
# TESTS

## ITEMS
@pytest.mark.usefixtures("delivery_client")
def test_get_items_without_filters(delivery_client, mock_items_response):
    r = delivery_client.get_content_items()
    item = r.items[0]
    assert item.codename == "about_us"
    assert r.count == 32
    assert r.api_response.ok == True


@pytest.mark.usefixtures("delivery_client")
def test_get_items_with_valid_filters(delivery_client, mock_items_with_filters_response):
    r = delivery_client.get_content_items(
        Filter("system.type", "[eq]", "coffee"),
        Filter("elements.price", "[range]", "10.5,50"),
        Filter("","depth", 6)
    )

    assert r.items[0].codename == "kenya_gakuyuni_aa"
    assert r.count == 1
    assert r.api_response.ok == True


@pytest.mark.usefixtures("delivery_client")
def test_get_items_with_invalid_filters(delivery_client, mock_items_with_filters_response):
    with pytest.raises(Exception):
        r = delivery_client.get_content_items(
            "fake", "filter", "here"
        )
        assert r == TypeError


@pytest.mark.usefixtures("delivery_client")
def test_get_item(delivery_client, mock_item_response):
    r = delivery_client.get_content_item("on_roasts")
    assert r.codename == "on_roasts"
    assert r.get_linked_items("related_articles")[0].codename == "coffee_processing_techniques"


@pytest.mark.usefixtures("delivery_client")
def test_get_linked_items_depth(delivery_client, mock_articles_response):
    r = delivery_client.get_content_items()
    c = r.items[1]
    level_1 = r.items[1].get_linked_items("related_articles")
    o = level_1[0]
    level_2 = level_1[0].get_linked_items("related_articles")
    a = level_2[1]
    level_3 = level_2[1].get_linked_items("related_articles")
    d = level_3[0]

    assert c.codename == "coffee_processing_techniques"
    assert o.codename == "on_roasts"
    assert a.codename == "origins_of_arabica_bourbon"
    assert d.codename == "donate_with_us"

## TYPES
@pytest.mark.usefixtures("delivery_client")
def test_get_article_type(delivery_client, mock_article_type_response):
    r = delivery_client.get_content_type("article")
    assert r.codename == "article"
    assert r.elements.title.name == "Title"
    assert r.elements.title.type == "text"
    assert r.elements.checkbox_choices.options[0].codename == "one"

@pytest.mark.usefixtures("delivery_client")
def test_get_types(delivery_client, mock_types_response):
    r = delivery_client.get_content_types()
    first_type = r.types[0]
    assert r.count >= 13
    assert first_type.codename == "about_us"
    assert first_type.elements.facts.name == "Facts"
    assert first_type.elements.facts.type == "modular_content"