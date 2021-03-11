import config
from delivery.client import DeliveryClient
from delivery.builders.filter_builder import Filter

## MANUAL TESTS
client = DeliveryClient(config.project_id, options=config.delivery_options)

items = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.price", "[range]", "10.5,50"),
    Filter("","depth", 6)
)

# RESULTS
if items:
    for item in items:
        print(item.name)