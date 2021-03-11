from delivery.builders.filter_builder import Filter, FilterBuilder
from delivery.builders.options_builder import DeliveryOptionsBuilder
from delivery.builders.url_builder import UrlBuilder
from delivery.request_manager import RequestManager
from delivery.content_item import ContentItem


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
        if response.status_code == 200:
            response = response.json()
            item_listing = [ContentItem(item["system"], item["elements"]) for item in response["items"]]

            return item_listing
        

    def get_content_item(self):
        pass
    def get_content_types(self):
        pass
    def get_content_type(self):
        pass
