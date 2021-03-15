import config
from delivery.client import DeliveryClient
from delivery.builders.filter_builder import Filter

## MANUAL TESTS
client = DeliveryClient(config.project_id, options=config.delivery_options)


## ITEMS
r = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.price", "[range]", "10.5,50"),
    Filter("","depth", 6)
)
# RESULTS
for item in r.items:
    print(item.name)
print(r.api_response.url)


## ITEM
r2 = client.get_content_item("on_roasts")
# RESULTS
print(r2.name)
print(r2.api_response.url)