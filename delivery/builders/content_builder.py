from delivery.content_item import ContentItem, ContentItemListing
from delivery.resolvers.content_link_resolver import ContentLinkResolver
from delivery.resolvers.inline_item_resolver import InlineItemResolver
from delivery.content_type import ContentType, ContentTypeListing
from delivery.taxonomy_group import TaxonomyGroup, TaxonomyGroupListing
from delivery.language import Language, LanguageListing

class ContentBuilder:
    def __init__(self):
        pass

    def build_content_item(self, delivery_client, response, item = None):
        json = response.json()
        if item is None:
            item = json["item"]
        if json["modular_content"]:
            item = ContentItem(item["system"], item["elements"], json["modular_content"], response)
        else:
            item = ContentItem(item["system"], item["elements"], response)
            
        if delivery_client.custom_link_resolver:
            item = ContentLinkResolver(delivery_client).resolve(item)

        if delivery_client.custom_item_resolver:
            item = InlineItemResolver(delivery_client).resolve(item)
        return item        

    def build_content_item_listing(self, delivery_client, response):
        json = response.json()
        items = [self.build_content_item(delivery_client, response, item) for item in json["items"]]
        content_item_listing = ContentItemListing(items, json["pagination"], json["modular_content"], response)          
        return content_item_listing


    def build_content_type(self, delivery_client, response, content_type = None):
        if content_type == None:
            content_type = response.json()
        content_type = ContentType(content_type["system"], content_type["elements"], response)
        return content_type

    
    def build_content_type_listing(self, delivery_client, response):
        json = response.json()
        content_types = [self.build_content_type(delivery_client, response, content_type) for content_type in json["types"]]
        content_type_listing = ContentTypeListing(content_types, json["pagination"], response)
        return content_type_listing


    def build_taxonomy_group(self, response, taxonomy_group = None):
        if taxonomy_group == None:
            taxonomy_group = response.json()
        taxonomy_group = TaxonomyGroup(taxonomy_group["system"], taxonomy_group["terms"], response)
        return taxonomy_group


    def build_taxonomy_group_listing(self, response):
        json = response.json()
        taxonomy_groups = [self.build_taxonomy_group(response, taxonomy_group) for taxonomy_group in json["taxonomies"]]
        taxonomy_group_listing = TaxonomyGroupListing(taxonomy_groups, json["pagination"], response)
        return taxonomy_group_listing


    def build_language(self, response, language = None):
        if language == None:
            language = response.json()
        language = Language(language["system"], response)
        return language


    def build_language_listing(self, response):
        json = response.json()
        languages = [self.build_language(response, language) for language in json["languages"]]
        language_listing = LanguageListing(languages, json["pagination"], response)
        return language_listing
    