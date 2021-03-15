from requests.models import Response
from delivery.content_item import ContentItem, ContentItemListing

class ListingBuilder:

    @staticmethod
    def build_content_item_listing(response:Response):
        json = response.json()
        items = [ContentItem(item["system"], item["elements"]) for item in json["items"]]
        content_item_listing = ContentItemListing(items, json["pagination"], json["modular_content"], response)          
        
        return content_item_listing