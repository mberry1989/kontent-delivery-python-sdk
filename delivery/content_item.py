from requests.models import Response


class ContentItem:
    def __init__(self, system:dict, elements:dict, api_response:Response = None):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.language = system["language"]
        self.content_type = system["type"]
        self.last_modified = system["last_modified"]
        self.collection = system["collection"]
        self.workflow_step = system["workflow_step"]
        self.elements = elements
        self.api_response = api_response

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

