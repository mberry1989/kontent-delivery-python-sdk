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


@pytest.fixture
def taxonomies_path():
    return "tests/fixtures/taxonomies.json"


@pytest.fixture
def taxonomy_path():
    return "tests/fixtures/taxonomy_group.json"


@pytest.fixture
def languages_path():
    return "tests/fixtures/languages.json"


@pytest.fixture
def feed_1_path():
    return "tests/fixtures/items_feed_1.json"


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


@pytest.fixture
def mock_taxonomy_response(monkeypatch, taxonomy_path):
    def mock_get(*args):
        return MockResponse(taxonomy_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)


@pytest.fixture
def mock_taxonomies_response(monkeypatch, taxonomies_path):
    def mock_get(*args):
        return MockResponse(taxonomies_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)


@pytest.fixture
def mock_languages_response(monkeypatch, languages_path):
    def mock_get(*args):
        return MockResponse(languages_path)
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)


@pytest.fixture
def mock_feed_response(monkeypatch, feed_1_path):
    def mock_get(*args):
        response = MockResponse(feed_1_path)
        response.headers = {"x-continuation": "test"}
        return response
    monkeypatch.setattr(RequestManager, 'get_request', mock_get)


# MOCK
class MockResponse:
    def __init__(self, path):
        self.ok = True
        self.path = path
        self.headers = None

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
    assert r.api_response.ok is True


@pytest.mark.usefixtures("delivery_client")
def test_get_items_with_valid_filters(delivery_client, mock_items_with_filters_response):
    r = delivery_client.get_content_items(
        Filter("system.type", "[eq]", "coffee"),
        Filter("elements.price", "[range]", "10.5,50"),
        Filter("", "depth", 6)
    )

    assert r.items[0].codename == "kenya_gakuyuni_aa"
    assert r.count == 1
    assert r.api_response.ok is True


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

### PREVIEW
@pytest.mark.usefixtures("delivery_client_with_options")
def test_get_preview_items(delivery_client_with_options, mock_articles_response):
    delivery_client_with_options.client_options.preview = True
    r = delivery_client_with_options.get_content_items()
    c = r.items[1]

    assert c.codename == "coffee_processing_techniques"

### SECURED
@pytest.mark.usefixtures("delivery_client_with_options")
def test_get_secured_items(delivery_client_with_options, mock_articles_response):
    delivery_client_with_options.client_options.secured = True
    r = delivery_client_with_options.get_content_items()
    c = r.items[1]

    assert c.codename == "coffee_processing_techniques"
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

## TAXONOMIES
@pytest.mark.usefixtures("delivery_client")
def test_taxonomy(delivery_client, mock_taxonomy_response):
    r = delivery_client.get_taxonomy("personas")
    assert r.codename
    assert len(r.terms) > 0

@pytest.mark.usefixtures("delivery_client")
def test_get_taxonomies(delivery_client, mock_taxonomies_response):
    r = delivery_client.get_taxonomies()
    assert r.count > 0
    assert len(r.taxonomy_groups) > 0

## LANGUAGES
@pytest.mark.usefixtures("delivery_client")
def test_languages(delivery_client, mock_languages_response):
    r = delivery_client.get_languages()
    assert len(r.languages) > 0

## ITEMS FEED
@pytest.mark.usefixtures("delivery_client")
def test_feed(delivery_client, mock_feed_response):
    r = delivery_client.get_content_items_feed(
        Filter("system.codename", "[eq]", "on_roasts")
    )

    items = r.feed.items
    feed_1_token = r.next
    next_result = r.get_next()

    assert len(items) > 0
    assert feed_1_token is not None
    assert next_result is not None
