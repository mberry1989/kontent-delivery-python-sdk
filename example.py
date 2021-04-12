import config
from delivery.client import DeliveryClient
from samples.custom_link_resolver import CustomLinkResolver
from delivery.builders.filter_builder import Filter

## MANUAL TESTS
client = DeliveryClient(config.project_id, options=config.delivery_options)
client.custom_link_resolver = CustomLinkResolver()


## ITEMS
r = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.price", "[range]", "10.5,50"),
    Filter("","depth", 6)
)
# RESULTS
for item in r.items: # array of ContentItems
    print(item.name) # getting the values
print(r.api_response.url)


## ITEM
r2 = client.get_content_item("coffee_processing_techniques")
# r2 = client.get_content_item("brisbane") # draft item for preview test

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
print(r2.elements.teaser_image.value[0].url)
### LINKED_ITEMS
print(r2.elements.related_articles.value) # codename array
print(r2.get_linked_items("related_articles")) # array of ContentItems
for item in r2.get_linked_items("related_articles"): # getting the item values
    print(f"name: {item.name} summary: {item.elements.summary.value}") 
## RICH TEXT VALUES
print(r2.elements.body_copy.value)
