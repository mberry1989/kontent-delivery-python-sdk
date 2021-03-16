from requests.models import Response
from delivery.content_item import ContentItem, ContentItemListing

class ContentBuilder:
    def __init__(self, response:Response):
        self.response = response
        self.json = response.json()

    def build_content_item(self):
        item = self.json["item"]
        if self.json["modular_content"]:
            item = ContentItem(item["system"], item["elements"], self.json["modular_content"], self.response)
        else:
            item = ContentItem(item["system"], item["elements"], self.response)
        return item        

    def build_content_item_listing(self):
        items = [ContentItem(item["system"], item["elements"]) for item in self.json["items"]]
        content_item_listing = ContentItemListing(items, self.json["pagination"], self.json["modular_content"], self.response)        
        
        return content_item_listing