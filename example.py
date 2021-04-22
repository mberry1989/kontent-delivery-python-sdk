import config
from delivery.client import DeliveryClient
from samples.custom_item_resolver import CustomItemResolver
from samples.custom_link_resolver import CustomLinkResolver
from delivery.builders.filter_builder import Filter
from delivery.builders.image_builder import ImageBuilder

# MANUAL TESTS
client = DeliveryClient(config.project_id, options=config.delivery_options)
client.custom_link_resolver = CustomLinkResolver()
client.custom_item_resolver = CustomItemResolver()


# ITEMS
r = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.price", "[range]", "10.5,50"),
    Filter("","depth", 6)
)
# RESULTS
for item in r.items: # array of ContentItems
    print(item.name) # getting the values
print(r.api_response.url)


# ITEM
r2 = client.get_content_item("coffee_processing_techniques")
r2 = client.get_content_item("brisbane") # draft item for preview test

# RESULTS
print(r2.codename)
### TEXT
print(r2.elements.title.value)
### MULTICHOICE
print(r2.elements.radio_choices.value[0].codename) # radio - one option possible
for check in r2.elements.checkbox_choices.value: # checkbox - multiple options possible
    print(check.codename)
### TAXONOMY
for persona in r2.elements.personas.value:
    print(persona.name)
### ASSET
asset_url = r2.elements.teaser_image.value[0].url
print(r2.elements.teaser_image.value[0].url)

image = ImageBuilder(asset_url)
transformed_image = image.transform(
    image.width(300),
    image.height(300),
    image.pixel_ratio(1.5),
    image.fit_mode("crop"),
    image.rect(100,100,0.7,0.7),
    image.focal_point(0.2,0.7,5),
    image.background_color("7A0099EE"),
    image.output_format("webp"),
    image.quality(85),
    image.lossless(True),
    image.auto_format_selection(False)
    )
print(transformed_image)

### LINKED_ITEMS
print(r2.elements.related_articles.value) # codename array
print(r2.get_linked_items("related_articles")) # array of ContentItems
for item in r2.get_linked_items("related_articles"): # getting the item values
    print(f"name: {item.name} summary: {item.elements.summary.value}") 
## RICH TEXT VALUES
print(r2.elements.body_copy.value)

### ITEMS FEED
r = client.get_content_items_feed()

while r.next:
    next_result = r.get_next()
    r.feed.items.extend(next_result.items)

for item in r.feed.items:
    print(item.name)
