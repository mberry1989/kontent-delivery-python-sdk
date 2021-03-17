import json
from requests.models import Response
from types import SimpleNamespace


class ContentItem:
    def __init__(self, system:dict, elements:dict, 
                modular_content = [], api_response:Response = None):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.language = system["language"]
        self.content_type = system["type"]
        self.last_modified = system["last_modified"]
        self.collection = system["collection"]
        self.workflow_step = system["workflow_step"]
        self.elements = json.loads(json.dumps(elements), object_hook=lambda d: SimpleNamespace(**d))
        self.modular_content = modular_content
        self.api_response = api_response

    def get_linked_items(self, element_codename):
        linked_codenames = getattr(self.elements, element_codename)
        linked_items = []
        for codename in linked_codenames.value:
            linked_item = self.modular_content[codename]
            linked_items.append(ContentItem(linked_item["system"], linked_item["elements"]))
        return linked_items

class ContentItemListing:
    def __init__(self, content_items:list, pagination:dict,
                    modular_content:dict, api_response:Response):
        self.items = content_items
        self.pagination = pagination
        self.skip = pagination["skip"]
        self.limit = pagination["limit"]
        self.count = pagination["count"]
        self.next_page = pagination["next_page"]
        self.modular_content = modular_content
        self.api_response = api_response

