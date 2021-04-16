from delivery.builders.content_builder import ContentBuilder
from delivery.builders.filter_builder import Filter, FilterBuilder
from delivery.builders.options_builder import DeliveryOptionsBuilder
from delivery.builders.url_builder import UrlBuilder
from delivery.request_manager import RequestManager


class DeliveryClient:
    def __init__(self, project_id, **options):
        self.project_id = project_id
        self.client_options = None
        if options:
            self.client_options = DeliveryOptionsBuilder().build_client_options(options)
        self.custom_link_resolver = None
        self.custom_item_resolver = None
        self.url_builder = UrlBuilder()
        self.request_manager = RequestManager()

        # TODO: performance - DRY - initialize builders in Client then use methods
    
    
    def get_content_items(self, *filters: Filter):
        endpoint = "/items"
        if filters:
            query_string = FilterBuilder(filters).return_url
            url = self.url_builder.build_url(self, endpoint, query_string)
        else:
            url = self.url_builder.build_url(self, endpoint)
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_item_listing = ContentBuilder(response, self).build_content_item_listing()     
            return content_item_listing
        
        return response.status_code


    def get_content_item(self, codename:str):
        url = self.url_builder.build_url(self, f"/items/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_item = ContentBuilder(response, self).build_content_item()
            return content_item


    def get_content_types(self):
        url = self.url_builder.build_url(self, f"/types")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_type_listing = ContentBuilder(response, self).build_content_type_listing()
            return content_type_listing


    def get_content_type(self, codename:str):
        url = self.url_builder.build_url(self, f"/types/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_type = ContentBuilder(response, self).build_content_type()
            return content_type

    
    def get_taxonomies(self):
        url = self.url_builder.build_url(self, f"/taxonomies")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            taxonomy_listing = ContentBuilder(response, self).build_taxonomy_group_listing()
            return taxonomy_listing   


    def get_taxonomy(self, codename:str):
        url = self.url_builder.build_url(self, f"/taxonomies/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            taxonomy_group = ContentBuilder(response, self).build_taxonomy_group()
            return taxonomy_group

    
    def get_languages(self):
        url = self.url_builder.build_url(self, f"/languages")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            language_listing = ContentBuilder(response, self).build_language_listing()
            return language_listing 