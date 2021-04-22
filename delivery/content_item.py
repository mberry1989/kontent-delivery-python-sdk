import json
from requests.models import Response
from types import SimpleNamespace


class ContentItem:
    def __init__(self, system:dict, elements:dict, 
                 modular_content = {}, api_response:Response = None):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.language = system["language"]
        self.content_type = system["type"]
        self.last_modified = system["last_modified"]
        self.collection = system["collection"]
        # components do not have workflow steps
        if "workflow_step" in system:
            self.workflow_step = system["workflow_step"]
        self.elements = json.loads(json.dumps(elements), 
                                              object_hook=lambda d: SimpleNamespace(**d))
        self.modular_content = modular_content
        self.api_response = api_response

    def get_linked_items(self, element_codename:str):
        try:
            linked_codenames = getattr(self.elements, element_codename)
            linked_items = []
            for codename in linked_codenames.value:
                linked_item = self.modular_content[codename]  
                linked_items.append(ContentItem(linked_item["system"], linked_item["elements"], self.modular_content))
            return linked_items
        except Exception as e:
            print(f"Getting linked items failed with exception: {e}.")


class ContentItemListing:
    def __init__(self, content_items:list, pagination:dict,
                    modular_content:dict, api_response:Response):
        self.items = content_items
        self.pagination = pagination
        if pagination:
            self.skip = pagination["skip"]
            self.limit = pagination["limit"]
            self.count = pagination["count"]
            self.next_page = pagination["next_page"]
        self.modular_content = modular_content
        self.api_response = api_response

class ContentItemsFeed:
    def __init__(self, delivery_client, items:ContentItemListing, url):
        self.feed = items
        self.url = url
        self.__delivery_client = delivery_client
        self.next = None

    def get_next(self):
        if self.next != None:
            response = self.__delivery_client.request_manager.get_request(self.__delivery_client, self.url, self.next)
            if response.ok:
                next_results = self.__delivery_client.content_builder.build_content_item_listing(self.__delivery_client, response)
            if "x-continuation" in next_results.api_response.headers.keys():
                self.next = { "x-continuation" : next_results.api_response.headers["x-continuation"] }
            else:
                self.next = None
            
            return next_results

