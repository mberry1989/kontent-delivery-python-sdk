from kontent_delivery.content_item import ContentItem
import json
import pytest
from kontent_delivery.resolvers.content_link_resolver import ContentLinkResolver
from kontent_delivery.resolvers.inline_item_resolver import InlineItemResolver


@pytest.fixture
def sample_json():
    with open("tests/fixtures/coffee_processing_techniques.json") as f:
        data = json.load(f)
        return data


@pytest.fixture
def sample_content(sample_json):
    content_item = ContentItem(sample_json["item"]["system"], sample_json["item"]["elements"], sample_json["modular_content"])
    return content_item


@pytest.mark.usefixtures("delivery_client_with_resolvers")
def test_link_resolver(sample_content, delivery_client_with_resolvers):
    results = ContentLinkResolver(delivery_client_with_resolvers).resolve(sample_content)
    assert type(results) == ContentItem
    assert '<a data-item-id="80c7074b-3da1-4e1d-882b-c5716ebb4d25" href="/coffees/kenya-gakuyuni-aa">' in results.elements.body_copy.value


@pytest.mark.usefixtures("delivery_client_with_resolvers")
def test_item_resolver(sample_content, delivery_client_with_resolvers):
    results = InlineItemResolver(delivery_client_with_resolvers).resolve(sample_content)
    assert type(results) == ContentItem
    assert "<blockquote class='twitter-tweet' data-lang='en'data-theme=dark><a href=Test tweet></a></blockquote>" in results.elements.body_copy.value
