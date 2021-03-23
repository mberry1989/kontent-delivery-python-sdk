from requests.models import Response
from delivery.content_item import ContentItem, ContentItemListing
from delivery.resolvers.content_link_resolver import ContentLinkResolver
from delivery.resolvers.inline_item_resolver import InlineItemResolver
from delivery.content_type import ContentType, ContentTypeListing

class ContentBuilder:
    def __init__(self, response:Response, delivery_client = None):
        self.response = response
        self.json = response.json()
        self.delivery_client = delivery_client

    def build_content_item(self, item = None):
        if item is None:
            item = self.json["item"]
        if self.json["modular_content"]:
            item = ContentItem(item["system"], item["elements"], self.json["modular_content"], self.response)
        else:
            item = ContentItem(item["system"], item["elements"], self.response)
            
        if self.delivery_client.custom_link_resolver:
            item = ContentLinkResolver(self.delivery_client).resolve(item)

        if self.delivery_client.custom_item_resolver:
            item = InlineItemResolver(self.delivery_client).resolve(item)
        return item        

    def build_content_item_listing(self):
        items = [self.build_content_item(item) for item in self.json["items"]]
        content_item_listing = ContentItemListing(items, self.json["pagination"], self.json["modular_content"], self.response)        
        
        return content_item_listing

    def build_content_type(self, content_type = None):
        if content_type == None:
            content_type = ContentType(content_type["system"], content_type["elements"])
        return content_type
    
    def build_content_type_listing(self):
        content_types = [self.build_content_type(content_type) for content_type in self.json["types"]]
        content_type_listing = ContentTypeListing(content_types, self.json["pagination"], self.response)
        return content_type_listing