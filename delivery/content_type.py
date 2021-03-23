import json
from requests.models import Response
from types import SimpleNamespace

class ContentType:
    def __init__(self, system:dict, elements:dict):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.last_modified = system["last_modified"]
        self.elements = json.loads(json.dumps(elements), 
                                   object_hook=lambda d: SimpleNamespace(**d))

class ContentTypeListing:
    def __init__(self, content_types:list, pagination:dict,
                 api_response:Response):
        self.types = content_types
        self.pagination = pagination
        self.skip = pagination["skip"]
        self.limit = pagination["limit"]
        self.count = pagination["count"]
        self.next_page = pagination["next_page"]
        self.api_response = api_response