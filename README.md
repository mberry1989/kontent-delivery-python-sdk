# Kentico Kontent Python SDK

## Table of Contents
- [Installation](#Installation)
- [Creating a client](#Creating-a-client)
- [Requesting items](#Requesting-items)
  - [Filtering](#Filtering-content)
- [Resolving inline links](#Resolving-inline-links)
- [Resolving inline items and components](#Resolving-inline-items-and-components)


## Installation
To install the SDK from the Python Package Index use:  

``` pip install kontent-delivery-python-sdk ```

## Creating a client
To obtain content from Kentico Kontent, you will create an instance of DeliveryClient and pass it your Project ID:

```python
from delivery.client import DeliveryClient

client = DeliveryClient("7a11a58d-cd21-002c-cd34-30196c7a1103")
```

### Setting up config.py
Using a configuration file to pass API keys and client options when creating instances of DeliveryClient is recommended. This can be done by adding a _config.py_ file to the root of your project and importing it to your modules. 

The _config.py_ file should be in the JSON format as follows:
```json
project_id ="your_project_id"
delivery_options = {   
    "preview": False,
    "preview_api_key": "enter_key_here",
    "secured": False,
    "secured_api_key": "enter_key_here",
    "timeout": (4,7)
    }
```

Which can be imported and used to build your DelieryClient:
```python
import config
from delivery.client import DeliveryClient

client = DeliveryClient(config.project_id, options=config.delivery_options)
```

### Delivery options
| Option | Values Type | Description |
| --- | --- | --- |
| preview | bool | Determines whether client will use [Kontent's Preview API](https://docs.kontent.ai/reference/delivery-api#section/Production-vs.-Preview) |
| preview_api_key | string | Project Preview API key 
| secured | bool | Determines whether client will use [Kontent's Secure access API](https://docs.kontent.ai/reference/delivery-api#tag/Secure-access) |
| secured_api_key | string | Project Secure access API key  |
| timeout | set | Determines (in seconds) the _read_ and _connect_ timeout threshold for the [Python "Requests" library](https://2.python-requests.org/en/master/user/advanced/#timeouts)

**Note:** Preview and Secured API cannot be enabled simultaneously. 


## Requesting items

### Getting a single item
Getting an item from Kontent can be accomplished by using the DeliveryClient's __get_content_item__ method and passing in the content item's codename:
```python
response = client.get_content_item("coffee_processing_techniques")

print(response.codename)
print(response.elements.title.value)

# prints:
# coffee_processing_techniques
# Coffee processing techniques
```

Using this method will return a **ContentItem**.  To access elements and their values use dot notation in the format: 
```response.elements.element_name.value``` 


#### ContentItem attributes:
| Attribute | Description |
| --- | --- | 
| id | An identifying GUID. |
| name | The item's display name as seen in the Kontent UI.|
| codename | A unique identifying codename set in the Kontent UI. **Note:** Special characters are replaced with "_".|
| language | The language that the returned item variant exists in. |
| content_type | The content model used by the returned item.|
| last_modified | The date the item was last editting in the Kontent UI.|
| collection | The Collection the item is assigned to. |
| workflow_step | The step the item is currently in. Note: Non-preview calls will only returned Published items.|
| modular_content| Linked items and components associated to the returned item.|
| api_response | Response object from the request.|

### Getting multiple items
Getting an item listing from Kontent can be accomplished by using the DeliveryClient's __get_content_items__ method:

```python
response = client.get_content_items()

for item in response.items:
    print(item.name)
    # prints:
    # About us
    # AeroPress
    # AeroPress Filters
    # ...
```
Using the DeliveryClient's __get_content_items__ method will produce a **ContentItemListing** object that stores each retrieved item as a **ContentItem** in an "items" attribute.  
#### ContentItemListing attributes:
| Attribute | Description |
| --- | --- |
| pagination | Dictionary containing the skip, limit, count, and next page parameters.|
| skip | Sets the number of objects to skip when requesting a list of objects.|
| limit | Sets the number of objects to retrieve in a single request.|
| count | The number of items in the response. |
| next_page | Contains the next page of results.|
| modular_content | Collection of all linked items and components refrenced in the request.|
| api_response | Response object from the request.|

### Filtering content
Filtering can be used when getting multiple items. Filters use an "element", "operation", "value" pattern such as the following filter to get any items with the title "On Roasts":

```python
response = client.get_content_items(
    Filter("elements.title", "[eq]", "On Roasts")
)
```

Filters can also be used for Kontent's Projection and parameters following the same pattern.  If there is no element to act upon, the Filter's first value is empty:

```python
Filter("", "depth", 6)
```
**Filters:**
| Operator | Description | Example |
| --- | --- | --- |
| [eq] |Property value equals the specified value.| ```Filter("system.type", "[eq]", "coffee")```|
| [neq] |Property value does not equal the specified value.|```Filter("elements.product_name", "[neq]", "Folgers")``` |
| [empty] |Property value is empty.|```Filter("elements.altitude", "[empty]", "")```|
| [nempty] |Property value is not empty.|```Filter("elements.country", "[nempty]", "")``` |
| [lt] |Property value is less than the specified value.|```Filter("price", "[lt]", "100")``` |
| [lte] |Property value is less than or equal to the specified value.|```Filter("price", "[lte]", "10.5")``` |
| [gt] |Property value is greater than the specified value.|```Filter("price", "[gt]", "5")``` |
| [gte] |Property value is greater than or equal to the specified value.|```Filter("price", "[gte]", "10.5")``` |
| [range] |Property value falls within the specified range of two values, both inclusive.|```Filter("elements.price", "[range]", "10.5,50")``` |
| [in] |Property value is in the specified list of values.|```Filter("elements.country", "[in]", "Kenya,Brazil,Argentina"``` |
| [nin] |Property value is not in the specified list of values.|```Filter("elements.country", "[nin]", "France")``` |
| [contains] |Property with an array of values contains the specified value.|```Filter("elements.product_status", "[contains]", "bestseller")``` |
| [any] |Property with an array of values contains at least one value from the specified list of values.|```Filter("elements.processing", "[any]", "wet__washed_,semi_dry")``` |
| [all] |Property with an array of values contains all of the specified values.|```Filter("elements.sitemap", "[all]", "coffee,products")``` |  
  
 **Parameters and Projection:**
| Operator | Description | Example |
| --- | --- | --- |
| depth |Content items can reference other content items using linked items or rich text elements. These linked items can reference other items recursively. By default, the API returns only one level of linked items.|```Filter("", "depth", 6) ``` |
| elements | When getting content items or content types, you can specify which elements to return by using the elements query parameter. | ```Filter("","elements","product_name")``` |

**Multiple filters and parameters can be passed into a single call:**
```python
response = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.product_name", "[neq]", "Folgers"),
    Filter("price", "[lte]", "10.5"),
    Filter("elements.country", "[in]", "Kenya,Brazil,Argentina"),
    Filter("","depth", 6),
    Filter("","elements","product_name")
)
```
## Rich Text Resolution
Rich Text Elements in Kontent can contain inline references to other content items within the project using links, inline content items, or components. To accomplish this using the Python SDK you need to:
1. Create a custom resolver
2. Import your custom resolver
3. Register the resolver with your DeliveryClient

Once a custom resolver is implemented and registered to the client, resolution will automatically happen when a ContentItem or ContentItemListing is built.

### Resolving inline links
By default, Kentico Kontent returns inline content item links with an empty "href" attribute and a "data-item-id" attribute containing the content item ID:
```html
<!-- inline content item link -->
<a data-item-id=\"80c7074b-3da1-4e1d-882b-c5716ebb4d25\" href=\"\">
```
To resolve the link, create a CustomLinkResolver that uses the **resolve_link()** method to evaluate and return an href string value:
```python
class CustomLinkResolver:
    @staticmethod
    def resolve_link(link):
        if link.type == "coffee":
            return f"/coffees/{link.url_slug}"
            
        if link.type == "article":
            return f"/articles/{link.url_slug}"
```
The _link_ argument passed into **resolve_link()** allows you to access the link type, codename, and url_slug.

Once a custom link resolver is implemented, import it and register to your DeliveryClient:
```python
from delivery.client import DeliveryClient
# namespace for your custom resolver will vary
from samples.custom_link_resolver import CustomLinkResolver

client = DeliveryClient("your_project_id")
client.custom_link_resolver = CustomLinkResolver()
```

### Resolving inline items and components
By default, Kentico Kontent returns inline content items and components links as objects with identifying attributes like "data-type" and "data-codename." This attributes are used to identify the inline item:  

```html
<!-- Inline Content Item: -->
<object type=\"application/kenticocloud\" data-type=\"item\" data-rel=\"link\" data-codename=\"on_roasts\"></object>
<!-- Component: -->
<object type=\"application/kenticocloud\" data-type=\"item\" data-rel=\"component\" data-codename=\"n71d0469e_9a77_0168_8f49_08f6d3bcaca3\"></object>
```
To resolve the inline item or component, create a CustomItemResolver that uses the **resolve_item()** method to replace the object elements:
```python
class CustomItemResolver:
    @staticmethod
    def resolve_item(linked_item):
        if linked_item.content_type == "article":
            return f"<h1>{linked_item.elements.title.value}</h1>"
            
        if linked_item.content_type == "tweet":
            return (f"<blockquote class='twitter-tweet' data-lang='en'"
                    f"data-theme={linked_item.elements.theme.value[0].codename}>"
                    f"<a href={linked_item.elements.tweet_link.value}></a></blockquote>")
```
The _linked_item_ argument passed into **resolve_item()** is a [ContentItem](#ContentItem-attributes). 

Once a custom link resolver is implemented, import it and register to your DeliveryClient:  
```python
from delivery.client import DeliveryClient
# namespace for your custom resolver will vary
from samples.custom_item_resolver import CustomItemResolver

client = DeliveryClient(config.project_id, options=config.delivery_options)
client.custom_item_resolver = CustomItemResolver()

```