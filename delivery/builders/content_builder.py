from requests.models import Response
from delivery.content_item import ContentItem, ContentItemListing

class ContentBuilder:
    def __init__(self, response:Response):
        self.response = response
        self.json = response.json()

    def build_content_item(self):
        item = ContentItem(self.json["item"]["system"], self.json["item"]["elements"], self.response)
        return item        

    def build_content_item_listing(self):
        items = [ContentItem(item["system"], item["elements"]) for item in self.json["items"]]
        content_item_listing = ContentItemListing(items, self.json["pagination"], self.json["modular_content"], self.response)        
        
        return content_item_listing