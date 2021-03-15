import config
from delivery.client import DeliveryClient
from delivery.builders.filter_builder import Filter
from delivery.content_item import ContentItem

## MANUAL TESTS
client = DeliveryClient(config.project_id, options=config.delivery_options)

r = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.price", "[range]", "10.5,50"),
    Filter("","depth", 6)
)

# RESULTS
for item in r.items:
    print(item.name)
print(r.api_response.url)