from requests.models import Response
from delivery.content_item import ContentItem, ContentItemListing
from delivery.resolvers.content_link_resolver import ContentLinkResolver
from delivery.resolvers.inline_item_resolver import InlineItemResolver

class ContentBuilder:
    def __init__(self, response:Response, delivery_client):
        self.response = response
        self.json = response.json()
        self.delivery_client = delivery_client

    def build_content_item(self):
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
        items = [ContentItem(item["system"], item["elements"]) for item in self.json["items"]]
        content_item_listing = ContentItemListing(items, self.json["pagination"], self.json["modular_content"], self.response)        
        
        return content_item_listing