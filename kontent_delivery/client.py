from kontent_delivery.builders.content_builder import ContentBuilder
from kontent_delivery.builders.filter_builder import Filter, FilterBuilder
from kontent_delivery.builders.options_builder import DeliveryOptionsBuilder
from kontent_delivery.builders.url_builder import UrlBuilder
from kontent_delivery.request_manager import RequestManager


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
        self.content_builder = ContentBuilder()
        self.filter_builder = FilterBuilder()

    def get_content_items(self, *filters: Filter):
        endpoint = "/items"
        if filters:
            query_string = self.filter_builder.build_return_url(filters)
            url = self.url_builder.build_url(self, endpoint, query_string)
        else:
            url = self.url_builder.build_url(self, endpoint)
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_item_listing = self.content_builder.build_content_item_listing(self, response)
            return content_item_listing

    def get_content_item(self, codename: str):
        url = self.url_builder.build_url(self, f"/items/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_item = self.content_builder.build_content_item(self, response)
            return content_item

    def get_content_types(self):
        url = self.url_builder.build_url(self, "/types")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_type_listing = self.content_builder.build_content_type_listing(self, response)
            return content_type_listing

    def get_content_type(self, codename: str):
        url = self.url_builder.build_url(self, f"/types/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_type = self.content_builder.build_content_type(self, response)
            return content_type

    def get_taxonomies(self):
        url = self.url_builder.build_url(self, "/taxonomies")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            taxonomy_listing = self.content_builder.build_taxonomy_group_listing(response)
            return taxonomy_listing

    def get_taxonomy(self, codename: str):
        url = self.url_builder.build_url(self, f"/taxonomies/{codename}")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            taxonomy_group = self.content_builder.build_taxonomy_group(response)
            return taxonomy_group

    def get_languages(self):
        url = self.url_builder.build_url(self, "/languages")
        response = self.request_manager.get_request(self, url)
        if response.ok:
            language_listing = self.content_builder.build_language_listing(response)
            return language_listing

    def get_content_items_feed(self, *filters: Filter):
        endpoint = "/items-feed"
        if filters:
            query_string = self.filter_builder.build_return_url(filters)
            url = self.url_builder.build_url(self, endpoint, query_string)
        else:
            url = self.url_builder.build_url(self, endpoint)
        response = self.request_manager.get_request(self, url)
        if response.ok:
            content_items_feed = self.content_builder.build_items_feed(self, response, url)
            return content_items_feed
