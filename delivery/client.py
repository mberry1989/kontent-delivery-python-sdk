from delivery.builders.listing_builder import ListingBuilder
from delivery.builders.filter_builder import Filter, FilterBuilder
from delivery.builders.options_builder import DeliveryOptionsBuilder
from delivery.builders.url_builder import UrlBuilder
from delivery.request_manager import RequestManager


class DeliveryClient:
    def __init__(self, project_id, **options):
        self.project_id = project_id
        self.client_options=None
        if options:
            self.client_options = DeliveryOptionsBuilder().build_client_options(options)
    
    def get_content_items(self, *filters: Filter):
        endpoint = "/items"
        if filters:
            query_string = FilterBuilder(filters).return_url
            url = UrlBuilder().build_url(self, endpoint, query_string)
        else:
            url = UrlBuilder().build_url(self, endpoint)
        response = RequestManager().get_request(self, url)
        if response.ok:
            content_item_listing = ListingBuilder().build_content_item_listing(response)     
            return content_item_listing
        
        return response.status_code
        

    def get_content_item(self):
        pass
    def get_content_types(self):
        pass
    def get_content_type(self):
        pass
