# Kentico Kontent Python SDK

![Build & Test](https://github.com/kentico-michaelb/kontent-delivery-python-sdk/actions/workflows/python-package.yml/badge.svg)

## Table of Contents
- [Installation](#Installation)
- [Creating a client](#Creating-a-client)
  -[Setting up config.py](#Setting-up-config.py)
  -[Delivery options](#Delivery-options)
  -[Retrying requests](#Retrying-requests)
- [Requesting items](#Requesting-items)
  - [Getting a single item](#Getting-a-single-item)
  - [Getting multiple items](#Getting-multiple-items)
  - [Filtering content](#Filtering-content)
- [Rich Text Resolution](#Rich-text-resolution)
  - [Resolving inline links](#Resolving-inline-links)
  - [Resolving inline items and components](#Resolving-inline-items-and-components)
- [Enumerating all items](#Enumerating-all-items)
- [Requesting content types](#Requesting-content-types)
  - [Getting a content type](#Getting-a-content-type)
  - [Getting multiple content types](#Getting-multiple-content-types)
- [Requesting Taxonomies](#Requesting-taxonomies)
  - [Getting a taxonomy group](#Getting-a-taxonomy-group)
  - [Getting multiple taxonomies](#Getting-multiple-taxonomies)
- [Listing languages](#Listing-languages)
- [Transforming images](#Transforming-images)


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

### **Delivery options**
| Option | Values Type | Description |
| --- | --- | --- |
| preview | bool | Determines whether client will use [Kontent's Preview API](https://docs.kontent.ai/reference/delivery-api#section/Production-vs.-Preview) |
| preview_api_key | string | Project Preview API key 
| secured | bool | Determines whether client will use [Kontent's Secure access API](https://docs.kontent.ai/reference/delivery-api#tag/Secure-access) |
| secured_api_key | string | Project Secure access API key  |
| timeout | set | Determines (in seconds) the _read_ and _connect_ timeout threshold for the [Python "Requests" library](https://2.python-requests.org/en/master/user/advanced/#timeouts)
| retry_attempts | int | Determines the number of times the SDK will [Retry](#) the request |

**Note:** Preview and Secured API cannot be enabled simultaneously. 

### Retrying requests
By default, the SDK uses a retry policy, asking for requested content again in case of an error. The default policy retries the HTTP request if the following status codes are returned:

 - 408 - RequestTimeout
 - 429 - TooManyRequests
 - 500 - InternalServerError
 - 502 - BadGateway
 - 503 - ServiceUnavailable
 - 504 - GatewayTimeout

The SDK will perform a total of 6 attempts at a maximum of 32 seconds to retrieve content before returning a max retry error. The consecutive attempts are delayed with exponential backoff.

To disable the retry policy or set a custom number of attempts, you can set  __retry_attempts__ in the config file:

```json
project_id ="your_project_id"
delivery_options = {   
    "retry_attempts": 0
    }

```

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


#### **ContentItem attributes:**
| Attribute | Description |
| --- | --- | 
| id | An identifying GUID. |
| name | The item's display name as seen in the Kontent UI.|
| codename | A unique identifying codename set in the Kontent UI. **Note:** Special characters are replaced with "_".|
| language | The language that the returned item variant exists in. |
| content_type | The content model used by the returned item.|
| last_modified | The date the item was last editted in the Kontent UI.|
| collection | The Collection the item is assigned to. |
| workflow_step | The step the item is currently in. Note: Non-preview calls will only returned Published items.|
| elements | Contains the content item values and element type information.|
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
Using the DeliveryClient's __get_content_items__ method will produce a **ContentItemListing** object that stores each retrieved item as a [**ContentItem**](#ContentItem-attributes) in an "items" attribute.  
#### **ContentItemListing attributes:**
| Attribute | Description |
| --- | --- |
| items | Contains the items returned in the response.|
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
#### **Filters:**
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
| [any] |Property with an array of values contains at least one value from the specified list of values.|```Filter("elements.processing", "[any]", ["wet__washed_","semi_dry"])``` |
| [all] |Property with an array of values contains all of the specified values.|```Filter("elements.sitemap", "[all]", ["coffee","products"])``` |  
  
#### **Parameters and Projection:**
| Operator | Description | Example |
| --- | --- | --- |
| depth |Content items can reference other content items using linked items or rich text elements. These linked items can reference other items recursively. By default, the API returns only one level of linked items.|```Filter("", "depth", 6) ``` |
| elements | When getting content items or content types, you can specify which elements to return by using the elements query parameter. | ```Filter("","elements",["name",product_name"])``` |
| skip | Sets the number of objects to skip when requesting a list of objects. The skip parameter must be combined with the limit parameter to work.  | ```Filter("", "skip", 2) ``` |
| limit | Sets the number of objects to retrieve in a single request. | ```Filter("", "limit", 10) ``` |
| language | Determines which language variant of content items to return. | ```Filter("", "language", "en-US") ``` |
| order | Determines the order of the retrieved objects. Use [asc] for ascending and [desc] for descending orders. | ```Filter("", "order","codename[desc]") ``` |

**Multiple filters and parameters can be passed into a single call:**
```python
response = client.get_content_items(
    Filter("system.type", "[eq]", "coffee"),
    Filter("elements.product_name", "[neq]", "Folgers"),
    Filter("price", "[lte]", "10.5"),
    Filter("elements.country", "[in]", ["Kenya","Brazil","Argentina"]),
    Filter("","depth", 6),
    Filter("","elements","product_name")
)
```
## Rich text resolution
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
## Enumerating all items
When enumerating all items in the specified project, or if exceeding the item response limit on the Delivery API's  __items__ endpoint is necessary, the [__items-feed__](https://docs.kontent.ai/reference/delivery-api#operation/enumerate-content-items) endpoint can be used. 

Getting an item feed from Kontent can be accomplished by using the DeliveryClient's __get_content_items_feed__ method:

```python
r = client.get_content_items_feed()

while r.next:
    next_result = r.get_next()
    r.feed.items.extend(next_result.items)

for item in r.feed.items:
    print(item.name)
    # prints:
    # Example Item Name 001
    # Example Item Name 002
    # ...
    # Example Item Name 4300
    # etc.
```

Using the DeliveryClient's __get_content_items_feed__ method will produce a **ContentItemsFeed** object that stores  [**ContentItemListing**](#ContentItemListing-attributes) objects in a "feed" attribute. Paginated results can be retrieved by using the __get_next__ method, which returns a **ContentItemListing** object.

#### **ContentItemFeed attributes:**
| Attribute | Description |
| --- | --- |
| feed | Contains ContentItemListing objects from the first page of the response, and can be extended using the ```get_next()``` method|
| url |  Contains the requested url.|
| next | Stores the "x-continuation" header for retrieving the next page of results. Set to ```None``` when no more pages are available. |  

[**Filtering**](#Filtering-content) can also be used when getting content item feeds:

```python
r = client.get_content_items_feed(
    Filter("system.codename", "[eq]", "test999")
)

print(r.url)
# prints: ~/items-feed?system.codename[eq]=on_roasts
```

## Requesting content types

### Getting a content type
Getting a content type from Kontent can be accomplished by using the DeliveryClient's __get_content_type__ method and passing in the content type's codename:
```python
response = client.get_content_type("article")

print(response.codename)
print(response.elements.body_copy)
print(response.elements.body_copy.name)

# prints:
# article
# namespace(type='rich_text', name='Body Copy')
# Body Copy
```

Using this method will return a **ContentType**.  To access elements and their values use dot notation in the format: 
```response.elements.element_name.attribute_name``` 


#### **ContentType attributes:**
| Attribute | Description |
| --- | --- | 
| id | An identifying GUID. |
| name | The type's display name as seen in the Kontent UI.|
| codename | A unique identifying codename set in the Kontent UI. **Note:** Special characters are replaced with "_".|
| last_modified | The date the type was last editted in the Kontent UI.|
| elements | Contains the content type elements.|
| api_response | Response object from the request.|  


### Getting multiple content types
Getting a type listing from Kontent can be accomplished by using the DeliveryClient's __get_content_types__ method:

```python
response = client.get_content_types()

for content_type in response.types:
    print(content_type.name)
    # prints:
    # About us
    # Accessory
    # Article
    # ...
```
Using the DeliveryClient's __get_content_types__ method will produce a **ContentTypeListing** object that stores each retrieved item as a **ContentType** in the "types" attribute.  
#### **ContentTypeListing attributes:**
| Attribute | Description |
| --- | --- |
| content_types | Contains the listing of project content types.|
| pagination | Dictionary containing the skip, limit, count, and next page parameters.|
| skip | Sets the number of objects to skip when requesting a list of objects.|
| limit | Sets the number of objects to retrieve in a single request.|
| count | The number of items in the response. |
| next_page | Contains the next page of results.|
| api_response | Response object from the request.|  

## Requesting taxonomies

### Getting a taxonomy group
Getting a taxonomy group from Kontent can be accomplished by using the DeliveryClient's __get_taxonomy__ method and passing in the taxonomy group's codename:
```python
response = client.get_taxonomy("personas")

print(response.codename)
print(response.terms)
print(response.terms[0].codename)
# prints:
# personas
# [namespace(name='Coffee expert', codename='coffee_expert', terms=[namespace(name='Barista', codename='barista', terms=[]) ...
# coffee_expert

```

Using this method will return a **TaxonomyGroup**.  To access terms and their values use dot notation in the format: 
```response.terms[list_postion].attribute_name``` 

You can get term and nested term values by looping through the terms lists or chaining together __.terms[list_postion]__:
```python
for term in response.terms:
    print(term.name)
    # prints:
    # Coffee expert
    # Coffee enthusiast
    # ...
print(response.terms[0].terms[0].codename)
# prints:
# barista
```

#### **TaxonomyGroup attributes:**
| Attribute | Description |
| --- | --- | 
| id | An identifying GUID. |
| name | The type's display name as seen in the Kontent UI.|
| codename | A unique identifying codename set in the Kontent UI. **Note:** Special characters are replaced with "_".|
| last_modified | The date the type was last editted in the Kontent UI.|
| terms | Taxonomy group terms containing name, codename, and nested terms.|
| api_response | Response object from the request.|  

### Getting multiple taxonomies
Using the DeliveryClient's __get_taxonomies__ method will produce a **TaxonomyGroupListing** object that stores each retrieved item as a **TaxonomyGroup** in the "taxonomy_groups" attribute.  

#### **TaxonomyGroupListing attributes:**
| Attribute | Description |
| --- | --- |
| taxonomy_groups | Contains the listing of taxonomy groups.|
| pagination | Dictionary containing the skip, limit, count, and next page parameters.|
| skip | Sets the number of objects to skip when requesting a list of objects.|
| limit | Sets the number of objects to retrieve in a single request.|
| count | The number of items in the response. |
| next_page | Contains the next page of results.|
| api_response | Response object from the request.|

## Listing languages
Using the DeliveryClient's __get_languages__ method will produce a **LanguageListing** object that stores each retrieved language as a **Language** in the "languages" attribute.   

To access language values loop through the language listing and use dot notation: 
```python
for language in response.languages:
    print(language.name)
    # prints:
    # English (United States)
    # Spanish (Spain)
    # ...
```   

#### **LanguageListing attributes:**
| Attribute | Description |
| --- | --- |
| languages | Contains a list of languages.|
| pagination | Dictionary containing the skip, limit, count, and next page parameters.|
| skip | Sets the number of objects to skip when requesting a list of objects.|
| limit | Sets the number of objects to retrieve in a single request.|
| count | The number of languages in the response. |
| next_page | Contains the next page of results.|
| api_response | Response object from the request.|

#### **Language attributes:**
| Attribute | Description |
| --- | --- | 
| id | An identifying GUID. |
| name | The langauge's display name as seen in the Kontent UI.|
| codename | A unique identifying codename set in the Kontent UI. **Note:** Special characters are replaced with "_".|
| api_response | Response object from the request.|  


## Transforming images
When you've obtained the URL for an asset, you can use the Kontent [Image Transformation API](https://docs.kontent.ai/reference/image-transformation) to make on-the-fly modifications to the image.

To use this, create an instance of **ImageBuilder** and pass the desired transformation methods into the bulder's __.transform()__ method. Example:

```python
# Get content item
response = client.get_content_item("coffee_processing_techniques")

# Get asset url
asset_url = response.elements.teaser_image.value[0].url

# Transform image
image = ImageBuilder(asset_url)
transformed_image = image.transform(
    image.width(300),
    image.height(300),
    image.pixel_ratio(1.5),
    )

print(transformed_image)
# prints: ~/coffee-processing-techniques-1080px.jpg?w=300&h=300&dpr=1.5
```

| Method | Accepted Values | Example |
| --- | --- | --- |
| .width | positive integer, or float between 0 and 1 | ```.width(300)``` |
| .height | positive integer, or float between 0 and 1 | ```.height(300)``` |
| .pixel_ratio | float greater than 0 but less than 5 | ```.pixel_ratio(1.5)``` |
| .fit_mode | string with value "crop", "clip", or "scale" | ```.fit_mode("crop")``` |
| .rect | 4 integer values representing pixels or floats representing percentages | ```.rect(100,100,0.7,0.7)``` |
| .focal_point | 2 floats between 0 and 1 and one integer between 1 and 100 | ```.focal_point(0.2,0.7,5)``` |
| .background_color | string containing 3, 4, 6, or 8 characters | ```.background_color("7A0099EE")``` |
| .output_format | string with value in [this supported list](https://docs.kontent.ai/reference/image-transformation#a-format-parameter)| ```.output_format("webp")``` |
| .quality | integer between 1 to 100 | ```.quality(85)``` |
| .lossless | True, False, 0, or 1 | ```.lossless(True)``` |
| .auto_format_selection | True, False, 0, or 1 | ```.auto_format_selection(False)``` |  


